import os

from flask import Flask, request, jsonify, render_template, redirect, url_for,send_file
from faker import Faker
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import SyncGrant
from werkzeug.utils import secure_filename

app = Flask(__name__)
fake = Faker()


@app.route('/')
def index():
    return render_template('index.html')

# Add your Twilio credentials
@app.route('/token')
def generate_token():
    TWILIO_ACCOUNT_SID = 'AC35365bde941c1b5428f4bb90a08ea84e'
    TWILIO_SYNC_SERVICE_SID = 'IS585de14721619aecfb7234ec5fef8d7f'
    TWILIO_API_KEY = 'SK71ba068f1cb5a30115d4cf8e622ae88d'
    TWILIO_API_SECRET = 'Ux6nWcEJa9cft24u9KAkNmK7gv3Ka1f7'

    username = request.args.get('username', fake.user_name())

    # create access token with credentials
    token = AccessToken(TWILIO_ACCOUNT_SID, TWILIO_API_KEY, TWILIO_API_SECRET, identity=username)
    # create a Sync grant and add to token
    sync_grant_access = SyncGrant(TWILIO_SYNC_SERVICE_SID)
    token.add_grant(sync_grant_access)
    return jsonify(identity=username, token=token.to_jwt().decode())

# Write the code here
@app.route('/', methods=['POST'])
def download_text():
    np = request.form['text']
    with open('message.txt','w') as f:
        f.write(np)
    x = "message.txt"
    return send_file(x,as_attachment=True)    

    


if __name__ == "__main__":
    app.run(host='localhost', port='5001', debug=True)
