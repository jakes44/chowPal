'''
Various utility functions used in flask server
'''
import requests
import time
import os

import PIL
from PIL import Image
from PIL import ImageEnhance
from StringIO import StringIO

from ocr_utils import *

GOOGLE_IMG_URL="https://www.google.com/search?tbm=isch&q={query}"

THRESHOLD = 100 # datapoint needed before computing similarity
SIM_CUT_OFF = 0.2 # minimum similarity index required to be considered ``similar''

'''
structure and sanitize payload, it got dirty along the way
'''

def generate_did(restaurant, dish_name):
    # rest = (restaurant.split()).join("")
    rest = "".join(restaurant.split()).lower()
    dish = "".join(dish_name.split()).lower()


    # rest = str(restaurant.split()).lower()
    # dish = str(dish_name.split()).join("").lower()

    print rest+"+"+dish
    return rest+"+"+dish

def structure_payload(nasty_shit,session, db_manager):

    payload = {}

    payload['did'] = generate_did(session['restaurant'], nasty_shit[0][0])
    payload['name'] = nasty_shit[0][0]
    payload['blurb'] = db_manager.get_blurb(payload['did'])

    if not payload['blurb']:
        payload['blurb'] = "TODO"#wiki_find(payload['name'])

    if not payload['blurb']:
        payload['blurb'] = "Ask your waiter/waitress!"

    payload['health_info'] = db_manager.get_health(payload['did'])
    payload['rating'] = db_manager.get_score(payload['did'])
    payload['similarity_liked'] = they_liked(session['similars'], payload['did'], db_manager)

    return payload

def to_ascii(string):
    res = ""
    for char in string:
        if ord(char) < 0 or ord(char) >= 128:
            continue
        res += char
    return res

def get_next_item(page):
    start = page.find('rg_di')

    if start == -1:
        end_quote = 0
        link = None
        return link, end_quote

    else:
        start = page.find('class="rg_meta"')
        start_content = page.find('"ou"', start + 1)
        end_content = page.find(',"ow"', start_content + 1)
        content = str(page[start_content+6:end_content-1])
        return content, end_content

def get_first_n_results(keyword, n):
    url = GOOGLE_IMG_URL.format(query=keyword)
    #print "Downloading from " + url
    page = requests.get(url, headers={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"})
    page = page.text
    results = []

    link, index = get_next_item(page)
    #print link

    while link is not None and len(results) <= n:
        results.append(link)
        page = page[index:]
        link, index = get_next_item(page)

    return results

def get_gimage_link(keyword):
    #print(keyword)
    #print(type(keyword))
    keyword = to_ascii(keyword)
    #keyword = keyword.encode('ascii', 'ignore')
    return get_first_n_results(keyword, 1)[0]

def aggregate_orders(orders):
    '''
    returns a dictionary based on the list of orders that maps did -> aggregated
    score (+)
    '''
    out_dict = {}

    for did, rating in orders:
        if did not in out_dict:
            out_dict[did] = rating
        else:
            out_dict[did] += rating

    return out_dict

def compute_similarity(hist1, hist2):
    '''
    computes similarity between two history objects
    '''
    if len(hist1) < THRESHOLD or len(hist2) < THRESHOLD:
        return float('-inf')
    sim_score = 0
    for did in hist1:
        if did in hist2:
            score1 = hist1[did]
            score2 = hist2[did]

            if score1 * score2 > 0: # same sign
                sim_score += min(abs(score1), abs(score2))
            else: # diff sign
                sim_score -= abs(score1 - score2)

    sim_score /= len(hist1)
    sim_score /= len(hist2)

    return sim_score

def get_similarity_rankings(me, db_manager):
    """
    get_similarity_rankings: ranks the others in order of similarity to me

    Args:
        me (string): uid of user in question
        db_manager: database manager
    
    Returns:
        the list of others in order of similarity to me, from most similar to
        least similar
    """
    others = db_manager.get_all_uid()
    # others.remove(me)
    my_hist = aggregate_orders(db_manager.get_order_history(me))
    others_list = map(lambda uid:
            aggregate_orders(db_manager.get_order_history(uid)),
            others)

    others_scores = map(lambda hist: compute_similarity(hist, my_hist),
            others_list)

    return sorted(filter(lambda item: item[1] > SIM_CUT_OFF, zip(others,
        others_scores)), key=lambda item: item[1], reverse=True)

def they_liked(user_list, did, db_manager):
    '''returns if at least a majority of ppl in user_list liked a dish'''
    personal_scores = map(lambda u: db_manager.get_personal_score(u[0], did), user_list)

    liked = 0
    total = 0

    for score in personal_scores:
        total += 1
        if score > 0:
            liked += 1

    return (2 * liked > total)

def process_info(image, x, y, session, db_manager):

    # image = enhancer.enhance(2)

    # image.show()

    output = get_text_info(image)

    # draw = PIL.ImageDraw.Draw(image)

    # draw.ellipse([x-10, y-10, x+10, y+10], fill=255, outline=255)

    results = []

    for (sent, (l, t, w, h)) in output:
        # print sent
        if (y >= t and y <= t+h and x >= l and x <= l+w):
            # draw.rectangle([l, t, l+w, t+h], outline=255)
            image = image.crop((l,t,l+w,t+h))
            #image.show()
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(1.5)
            #image.show()
            other =  get_text_info(image, True)[0][0]
            results.append((other, get_first_n_results(other + " \"recipe\"", 4)))

    # image.show()
    
    # Structure this shit
    '''
    { did: asdfsdaf, < hash(restaurant+dish_name) <-- preprocessed, split->join .lower()
      name: result[0][0], 
      blurb: blurb here, <- try db_manager.get_blurb(did) except: wiki-find: finally: ask waiter?
      pics: results[0][1],
      health_info: {}, <- db_manager.get_health(did)
      rating: some aggregate score, <- db_manager.get_score(did)
      similarity_liked: bool <- }
    '''

    return structure_payload(results, session, db_manager)

if __name__ == '__main__':
    print get_gimage_link("bibimbap")
