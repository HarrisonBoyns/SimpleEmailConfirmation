from app.database.db import db
from typing import List, Dict, Union
from app.models.item_model import ItemJson

StoreJson = Dict[str, Union[int, str, List[ItemJson]]]

#  black is very good for formatting python
#  to run black run with "black ."
# use black and do typing


class StoreModel(db.Model):
    __tablename__ = "stores"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)

    items = db.relationship("ItemModel", lazy="dynamic")

    @classmethod
    def find_by_name(cls, name) -> StoreJson:
        return cls.query.filter_by(name=name).first()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_all(cls) -> List["StoreJson"]:
        return cls.query.all()

    @classmethod
    def delete_all(cls) -> None:
        return cls.query.delete()
