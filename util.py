'''
Various utility functions used in flask server
'''
import requests
import time
import os
import db_manager

from PIL import Image
from StringIO import StringIO

GOOGLE_IMG_URL="https://www.google.com/search?tbm=isch&q={query}"

THRESHOLD = 100 # datapoint needed before computing similarity
SIM_CUT_OFF = 0.2 # minimum similarity index required to be considered ``similar''

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

def get_similarity_rankings(me, others, db_manager):
    """
    get_similarity_rankings: ranks the others in order of similarity to me

    Args:
        me (string): uid of user in question
	others (list of string): list of uid they 
        db_manager: database manager
    
    Returns:
        the list of others in order of similarity to me, from most similar to
        least similar
    """
    my_hist = aggregate_orders(db_manager.get_order_history(me))
    others_list = map(lambda uid:
            aggregate_orders(db_manager.get_order_history(uid)),
            others)

    others_scores = map(lambda hist: compute_similarity(hist, my_hist),
            others_list)

    return sorted(filter(lambda item: item[1] > SIM_CUT_OFF, zip(others,
        others_scores)), key=lambda item: item[1], reverse=True)

def process_info(image, x, y):
    
    pass

if __name__ == '__main__':
    print get_gimage_link("bibimbap")
