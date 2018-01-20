'''
Various utility functions used in flask server
'''
import requests
import time
import os
import sqlite

from PIL import Image
from StringIO import StringIO

GOOGLE_IMG_URL="https://www.google.com/search?tbm=isch&q={query}"
db

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
    my_hist = db_manager.get_order_history()
    pass

def get_order_history(uid):
  db = sqlite3.connect('DB/chow.db')
  c = db.cursor()

  return c.execute("select did,rating from choices where uid=?",(uid,)).fetchall()


if __name__ == '__main__':
    print get_gimage_link("bibimbap")
