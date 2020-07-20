from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Mail, Message
import secrets
import os
import re

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.sqlite'
app.config['SECRET_KEY'] = os.environ.get('secret_key')

app.config.update(dict(
    DEBUG = True,
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 587,
    MAIL_USE_TLS = True,
    MAIL_USE_SSL = False,
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME'),
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD'),
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_USERNAME'),
    MAIL_ASCII_ATTACHMENTS = False
    ))


db = SQLAlchemy(app)
mail = Mail(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    token = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(120), nullable=False)



pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)+$'


@app.route('/')
def index():
    pass
   


@app.route('/your/data/<token>', methods=['GET'])
def get_data(token):
    user = User.query.filter_by(token=token).first()
    if token:
        return {
                "success": 200,
                "name": user.name,
                "email":user.email,
                "token":user.token,
                "id":user.id                
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


@app.route('/get_rates/<token>')
def get_rates(token):
    pass



@app.route('/blogs/<token>')
def predictions(token):
    pass

 
@app.route('/update/profile/<token>', methods=['POST'])
def edit_profile(token):
    user = User.query.filter_by(token=token).first()
    data = request.get_json()
    if user:
        name = data['name']
        email = data['email']
        if re.fullmatch(pattern, email):
            user.name = name
            user.email = email
            db.session.commit()
        
        else:
            return {
                    "messsage": "invalid email address, enter the correct email format"
                    }
        return {
                "message":"account updated"
            }
    else:
        return {
                "message": "token entered does not exist"
                }

@app.route('/get_token/<email>/<password>', methods=['POST'])
def get_token(email, password):
    if re.fullmatch(pattern, email):
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                return {
                        "token":user.token
                        }

            else:
                return {
                        "message": "wrong password or invalid credentials"
                        }
        else:
            return {
                    "messsage": "the email entered does not exist"
                    }
    else:
        return {
                "message": "invalid email format",
                "suggestion":"enter correct format e.g <yourname>@<xyz>.<xyz>"
                }


if __name__ == '__main__':
    app.run(debug=True)


