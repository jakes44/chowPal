'''
main server
'''

from flask import Flask, request, session, url_for, redirect

app = Flask(__name__)

session['UID'] = 0

@app.route("/")
def root():
    return ""

@app.route("/process_menu", methods=['GET', 'POST'])
def process_img():
    '''
    Handles OCR and returns relevant information in JSON format to frontend

    Activated when tapped on menu

    Necessary args in POST request:
        - UID
        - Img
        - Tapped coordinate
    '''
    pass

@app.route("/recommend", methods=['GET', 'POST'])
def recommend():
    '''
    Handles recommendation to user, relevant data in JSON format given to
    frontend

    Activated upon ``recommend'' feature being used

    Necessary args in POST request:
        - UID
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
        - UID
        - DID
        - type of feedback (good or bad)
    '''
    pass

@app.route("/review", method=['GET', 'POST'])
def review():
    '''
    Handles user review
    
    Necessary args in POST request:
        - UID
        - DID
        - star rating
    '''
    pass

if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 8000, debug = True)
