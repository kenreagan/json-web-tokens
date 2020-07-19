from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
import os
import re

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.sqlite'
app.config['SECRET_KEY'] = os.environ.get('secret_key')

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    token = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(120), nullable=False)



pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)+$'


@app.route('/')
def index():
    return {

            'message' : 'hello world'

            }


@app.route('/your/data/<token>', methods=['GET'])
def get_data(token):
    user = User.query.filter_by(token=token).first()
    if token:
        return {

                "success": 200,
                "name": user.name,
                "email":user.email,
                "token":user.token

                }

    else:
        return {

                "message": "invalid token"

                }
    

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    name = data['name']
    email = data['email']
    if re.fullmatch(pattern, email):
        newemail = email
        password = data['password']
        token = secrets.token_hex(12)
        details = User(name=name, email=newemail, password=generate_password_hash(password=password, method='sha256'), token=token)
        db.session.add(details)
        db.session.commit()
        return {
                "message": "account created for {0}".format(name),
                "status": 200,
                "token": token
              }
    else:
        return {
                 "message": "your email is not valid"
            }


if __name__ == '__main__':
    app.run(debug=True)


