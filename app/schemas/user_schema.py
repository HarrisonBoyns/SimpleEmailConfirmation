from app.ma import ma
from app.models.user_model import UserModel
# tells marshmallow that password will only be for loading data
# define a meta class class Meta:
# load_only = ('has_to_be_a_tuple',)

# flask marshmallow reduces the duplication. Means we no longer needs the fields defined in the UserSchema

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserModel
        load_only = ("password",)
        dump_only = ("id","activated")
        load_instance = True


#  to use flask marshmallow
# firstly create a Marshmallow object
# then import it into the desired schema file witht the desired model
# inherit from ma.SQLAlchemyAutoSchema and include in the meta the:
#         model = UserModel
#         load_only = ("password",)
#         dump_only = ("id")