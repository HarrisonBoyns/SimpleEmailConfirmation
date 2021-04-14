from flask import request
from flask_jwt_extended import (
    jwt_required,
    get_jwt,
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
)
from marshmallow import ValidationError

from app.schemas.user_schema import UserSchema
from flask_restful import Resource
from werkzeug.security import safe_str_cmp
from app.models.user_model import UserModel

BLACK_ERROR = "{} cannot be blank"
USER_NAME_EXISTS = "user with this username already exists"
USER_CREATED = "user created successfully"
USER_NOT_FOUND = "user not found"
DELETED = "deleted"
SUCCESS = "success"
INVALID_CREDENTIALS = "invalid credentials"
LOGGED_OUT = "Logged out"
NOT_CONFIRMED = "Account not activated please check email and confirm {}!"
USER_ACTIVATED = "User has been activated"

revoked_tokens = []

user_schema = UserSchema()


#  -- > shift + F6 to rename the data within the current scope
# --> to extract and maniuplate a variable use refeactor --> extract --> variable

class UserLogin(Resource):
    @classmethod
    def post(cls):
        user_data = user_schema.load(request.get_json())

        user = UserModel.find_by_username(user_data.username)

        if user and safe_str_cmp(user.password, user_data.password):
            if user.activated:
                access_token = create_access_token(identity=user.id, fresh=True)
                refresh_token = create_refresh_token(user.id)
                return {"access_token": access_token, "refresh_token": refresh_token}, 200
            return {"message": NOT_CONFIRMED.format(user.username)}
        return {"message": INVALID_CREDENTIALS}, 401


class UserRegister(Resource):
    def post(self):
        user_data = user_schema.load(request.get_json())

        item = UserModel.find_by_username(user_data.username)

        if item:
            return {"message": USER_NAME_EXISTS}, 400

        user_data.save_to_db()
        return {"message": USER_CREATED}


class AllUsers(Resource):
    def get(self):
        return [user_schema.dump(user) for user in UserModel.find_all()]


class UserResource(Resource):
    def get(self, id: int):
        user = UserModel.find_by_id(id)

        user_json = user_schema.dump(user)

        if user_json:
            return user_json
        else:
            return {"message": "user does not exist"}, 404

    @jwt_required()
    def delete(self, id: int):
        user = UserModel.find_by_id(id)
        if user:
            user.delete()
            return {"message": DELETED}, 200
        else:
            return {"message": USER_NOT_FOUND}, 404


class TokenRefresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        user = get_jwt()
        new_access_token = create_access_token(identity=user, fresh=False)
        return {"access_token": new_access_token}, 200


class UserLogOut(Resource):
    @classmethod
    @jwt_required()
    def post(cls):
        jti = get_jwt()["jti"]
        revoked_tokens.append(jti)
        return {"message": LOGGED_OUT}


class UserConfirm(Resource):
    @classmethod
    def get(cls, id: int):
        user = UserModel.find_by_id(id)
        if user:
            user.activated = True
            user.save_to_db()
            return {"message": USER_ACTIVATED}, 200
        return {"message": USER_NOT_FOUND}, 400
