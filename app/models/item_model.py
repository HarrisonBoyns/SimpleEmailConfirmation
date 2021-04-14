from app.database.db import db
from typing import Dict, List, Union

# to use complex types one must import them from the typing module
# used to help you hint. Doesn't cause program to crash
# place constants in a constant file --> good form

ItemJson = Dict[str, Union[int, str, float]]


class ItemModel(db.Model):
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True, unique=True)
    item = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float(precision=2), nullable=False)

    store_id = db.Column(db.Integer, db.ForeignKey("stores.id"), nullable=False)
    store = db.relationship("StoreModel")

    @classmethod
    def find_by_name(cls, name: str) -> "ItemModel":
        return cls.query.filter_by(item=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_all(cls) -> List:
        return cls.query.all()

    @classmethod
    def delete_all(cls):
        return cls.query.delete()
