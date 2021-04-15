from app.libs.ma import ma
from app.models.user_model import UserModel


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserModel
        load_only = ("password",)
        dump_only = ("id", "activated")
        load_instance = True
