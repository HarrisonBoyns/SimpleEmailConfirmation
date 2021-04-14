from app.database.db import db
from typing import Dict, Union, List

UserJson = Dict[str, Union[str, str]]

# with flask marshmallow one no longer needs the constructor as the flag nullable
# is false has been set

class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False,unique=True)
    password = db.Column(db.String(30), nullable=False)
    activated = db.Column(db.Boolean, default=False)

    @classmethod
    def find_by_username(cls, name: str) -> "UserModel":
        return cls.query.filter_by(username=name).first()

    @classmethod
    def find_all(cls) -> List["UserModel"]:
        return cls.query.filter_by()

    @classmethod
    def find_by_id(cls, _id: int) -> "UserModel":
        return cls.query.filter_by(id=_id).first()

    def delete(self) -> None:
        db.session.delete(self)
        db.session.commit()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()
