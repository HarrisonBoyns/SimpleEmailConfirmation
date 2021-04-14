from app.ma import ma
from app.models.item_model import ItemModel
from app.models.store_model import StoreModel

class ItemSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ItemModel
        load_only = ("store",)
        dump_only = ("id",)
        include_fk = True
        load_instance = True

