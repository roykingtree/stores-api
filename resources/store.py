from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.store import StoreModel


class Store(Resource):
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {'message': 'Could not find store by that name.'}, 404

    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'message': "Store already created."}, 400
        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {'message': 'Error while adding store to database.'}, 500
        return store.json(), 201

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            try:
                store.delete_from_db()
            except:
                return {'message': 'Error while deleting store from database.'}, 400
            return {'message': "Store deleted."}

        else:
            return {'message': 'Could not find store by that name.'}, 404


class StoreList(Resource):
    def get(self):
        return {'stores': [store.json() for store in StoreModel.query.all()]}
