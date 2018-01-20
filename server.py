'''
main server
'''

from flask import Flask, request, session, url_for, redirect, render_template

app = Flask(__name__)

@app.route("/")
def root():
    return render_template("index.html")

@app.route("/init", methods=['GET', 'POST'])
def ping():
    '''
    Initializes the session more or less

    Called when the session loads

    Necessary args in POST request:
        - UID
        - Geo-coordinate
    '''
    pass

@app.route("/process_menu", methods=['GET', 'POST'])
def process_img():
    '''
    Handles OCR and returns relevant information in JSON format to frontend

    Activated when tapped on menu

    Necessary args in POST request:
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
    app.run(host = "0.0.0.0", port = 8000, debug = True)
