from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource, reqparse
from app.models.item_model import ItemModel
from app.schemas.item_schema import ItemSchema

BLACK_ERROR = "{} cannot be blank"
ITEM_NOT_FOUND = "item not found"
ITEM_WITH_NAME_EXISTS = "item with this name already exists"
DELETED = "deleted"
SUCCESS = "success"

item_schema = ItemSchema()
item_list_schema = ItemSchema(many=True)

class Items(Resource):

    @classmethod
    def get(cls, name: str):
        item_json = ItemModel.find_by_name(name)
        if item_json is None:
            return {"message": ITEM_NOT_FOUND}, 404
        return {"item": item_schema.dump(item_schema.dump(item_json))}

    @classmethod
    @jwt_required()
    def post(cls, name: str):
        json_item = ItemModel.find_by_name(name)
        if json_item is not None:
            return {"message": ITEM_WITH_NAME_EXISTS}, 404
        json_item = item_schema.load(request.get_json())
        json_item.save_to_db()
        return item_schema.dump(json_item), 201

    @classmethod
    @jwt_required()
    def delete(cls, name: str):
        json_item = ItemModel.find_by_name(name)
        if json_item is None:
            return {"message": ITEM_NOT_FOUND}, 400
        json_item.delete_from_db()
        return {"message": DELETED}, 201

    @classmethod
    @jwt_required()
    def put(cls, name: str):
        json_item = ItemModel.find_by_name(name)
        json_data = item_schema.load(request.get_json())
        if json_item is None:
            json_item = json_data
        else:
            json_item.price = json_data.price
        json_item.save_to_db()
        return {"item": item_schema.dump(json_data)}, 200


class ItemList(Resource):
    @classmethod
    def get(self):
        return {"items": item_list_schema.dump(ItemModel.get_all())}, 200

    @classmethod
    @jwt_required()
    def delete(self):
        ItemModel.delete_all()
        return {"message": SUCCESS}, 200
