from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from marshmallow import ValidationError

from app.models.store_model import StoreModel
from app.schemas.store_schema import StoreSchema

BLACK_ERROR = "{} cannot be blank"
ITEM_NOT_FOUND = "item not found"
ITEM_WITH_NAME_EXISTS = "item with this name already exists"
DELETED = "deleted"
SUCCESS = "success"

store_schema = StoreSchema()
store_schema_list = StoreSchema(many=True)


class Store(Resource):
    @classmethod
    @jwt_required()
    def get(cls, name: str):
        store_json = StoreModel.find_by_name(name)
        if store_json is None:
            return {"message": ITEM_NOT_FOUND}, 404
        return {"store": store_schema.dump(store_json)}

    @classmethod
    @jwt_required()
    def post(cls, name: str):

        json_item = StoreModel.find_by_name(name)
        if json_item is not None:
            return {"message": ITEM_WITH_NAME_EXISTS}, 404
        store_item = store_schema.load(request.get_json())
        try:
            store_item.save_to_db()
        except:
            return {"message": "server error"}, 500
        return store_schema.dump(store_item), 200

    @classmethod
    @jwt_required()
    def delete(cls, name: str):
        store_model = StoreModel.find_by_name(name)

        if store_model is None:
            return {"message": ITEM_NOT_FOUND}, 400
        store_model.delete_from_db()
        return {"message": DELETED}, 201

    @classmethod
    @jwt_required()
    def put(cls, name: str):
        data = store_schema.load(request.get_json())
        store_model = StoreModel.find_by_name(name)
        if store_model is None:
            store_model = data
        else:
            store_model.name = data.name
        store_model.save_to_db()
        return {"item": store_schema.dump(store_model)}, 200


class StoreList(Resource):
    @classmethod
    @jwt_required()
    def get(cls):
        stores = store_schema_list.dump(StoreModel.get_all())
        return {"stores": stores}, 200

    @classmethod
    @jwt_required()
    def delete(cls):
        StoreModel.delete_all()
        return {"message": SUCCESS}, 200
