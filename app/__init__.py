from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager

from app.error_handling.handling import register_error_handling
from app.resources.store_resource import StoreList, Store
from app.resources.user_resource import (
    UserRegister,
    UserResource,
    UserLogin,
    TokenRefresh,
    revoked_tokens,
    UserLogOut,
    AllUsers,
    UserConfirm
)
from app.resources.items_resource import Items, ItemList
from app.callbacks.callbacks import register_callbacks
from marshmallow import ValidationError

app = Flask(__name__)

app.secret_key = "top_secret"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["PROPAGATE_EXCEPTIONS"] = True

api = Api(app)

jwt = JWTManager(app)

# register some decorators
register_callbacks(jwt)
register_error_handling(app)

api.add_resource(Items, "/items/<string:name>")
api.add_resource(ItemList, "/items")
api.add_resource(UserRegister, "/signup")
api.add_resource(Store, "/stores/<string:name>")
api.add_resource(StoreList, "/stores")
api.add_resource(UserResource, "/users/<int:id>")
api.add_resource(UserLogin, "/login")
api.add_resource(TokenRefresh, "/refresh")
api.add_resource(UserLogOut, "/logout")
api.add_resource(AllUsers, "/users")
api.add_resource(UserConfirm, "/confirm/<int:id>")
