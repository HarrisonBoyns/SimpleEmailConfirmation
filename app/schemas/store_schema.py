from app.ma import ma
from app.models.store_model import StoreModel
from app.schemas.item_schema import ItemSchema

class StoreSchema(ma.SQLAlchemyAutoSchema):
    items = ma.Nested(ItemSchema, many=True)
    class Meta:
        model = StoreModel
        dump_only = ("id",)
        load_instance = True
        include_fk = True
