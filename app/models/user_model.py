from flask import request, url_for
from requests import Response
from app.database.db import db
from typing import Dict, Union, List

from app.libs.mailgun import MailGun

UserJson = Dict[str, Union[str, str]]

class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    activated = db.Column(db.Boolean, default=False)

    @classmethod
    def find_by_username(cls, name: str) -> "UserModel":
        return cls.query.filter_by(username=name).first()

    @classmethod
    def find_by_email(cls, email: str) -> "UserModel":
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_all(cls) -> List["UserModel"]:
        return cls.query.filter_by()

    @classmethod
    def find_by_id(cls, _id: int) -> "UserModel":
        return cls.query.filter_by(id=_id).first()

    def send_confirmation_email(self):
        link = request.url_root[:-1] + url_for("userconfirm", id=self.id)
        html = link
        return MailGun.send_email(
            email=self.email, subject="confirmation email", message_body=link, html=html
        )

    def delete(self) -> None:
        db.session.delete(self)
        db.session.commit()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()
