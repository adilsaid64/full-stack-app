from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS


app = Flask(__name__)
CORS(app) # wrap the app in CORS. Disable cors errors to allow sending of cross origin reqquests to our app.


# Configure the database. Using a local database.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabse.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # does not track all modifications made to the databse. Makes life a little easier for development

db = SQLAlchemy(app) # craete DB instance to get access to the databse. ORM - object relational mapping.

