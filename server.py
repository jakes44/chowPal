'''
main server
'''

from flask import Flask, request, session, url_for, redirect, render_template
import json
import re
import cStringIO

from db_manager import DBManager

from PIL import Image

dbManager = DBManager("DB/chow.db")

from util import *

app = Flask(__name__)

@app.route("/")
def root():
    return render_template("index.html")

@app.route("/init", methods=['GET', 'POST'])
def ping():
    '''
    Initializes the session more or less

    Called when the session loads

    store restaurant info in session session['restaurant']
    store UID in session

    Necessary args in POST request:
        - UID
        - Geo-coordinate
    '''
    print request.form
    uid = request.form['uid']
    restaurant = request.form['restaurant']
    similares = get_similarity_rankings(uid, dbManager)

    session['uid'] = uid
    session['restaurant'] = restaurant
    session['similars'] = similares

    return ""

@app.route("/process_menu", methods=['GET', 'POST'])
def process_img():
    '''
    Handles OCR and returns relevant information in JSON format to frontend

    Activated when tapped on menu

    Necessary args in POST request:
        - Img
        - Tapped coordinate
    '''
    if request.method == 'GET':
        return json.dumps({'response': 'invalid call'})
    else:
        img = request.form['image']
        image_data = re.sub('^data:image/.+;base64,', '', img).decode('base64')
        image = Image.open(cStringIO.StringIO(image_data))
        x = int(request.form['x'])
        y = int(request.form['y'])

        out_result = process_info(image, x, y, session, dbManager)

    return json.dumps({'status': 'success', 'result': json.dumps(out_result)})

@app.route("/recommend", methods=['GET', 'POST'])
def recommend():
    '''
    Handles recommendation to user, relevant data in JSON format given to
    frontend

    Activated upon ``recommend'' feature being used

    Necessary args in POST request:
        - Img
        - Tapped coordinate
        - Mode
    '''
    pass

@app.route("/yes_no_feedback", methods=['GET', 'POST'])
def simple_feedback():
    '''
    Handles immediate yes/no feedback from the user
    
    Necessary args in POST request:
        - DID
        - type of feedback (good or bad)
    '''
    pass

@app.route("/review", methods=['GET', 'POST'])
def review():
    '''
    Handles user review
    
    Necessary args in POST request:
        - DID
        - star rating
    '''
    pass

if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(host = "0.0.0.0", port = 8000, debug = True)

