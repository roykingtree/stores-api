import os
from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList
from db import db

application = Flask(__name__)

if 'RDS_HOSTNAME' in os.environ:
      DATABASE = {
        'NAME': os.environ['RDS_DB_NAME'],
        'USER': os.environ['RDS_USERNAME'],
        'PASSWORD': os.environ['RDS_PASSWORD'],
        'HOST': os.environ['RDS_HOSTNAME'],
        'PORT': os.environ['RDS_PORT'],
      }
      database_url = 'postgres://%(USER)s:%(PASSWORD)s@%(HOST)s:%(PORT)s/%(NAME)s' % DATABASE
else:
    database_url = 'sqlite:///data.db'

application.config['SQLALCHEMY_DATABASE_URI'] = database_url
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
application.secret_key = 'roy'
api = Api(application)
db.init_app(application)


@application.before_first_request
def create_tables():
    db.create_all()


jwt = JWT(application, authenticate, identity)  # /auth

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')

if __name__ == '__main__':
    application.run(port=5000, debug=True)
