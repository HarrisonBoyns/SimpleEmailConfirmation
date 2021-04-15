import requests
from typing import List
import os

from requests import Response

from app.error_handling.error_handling import MailGunException


class MailGun:

    MAILGUN_DOMAIN = os.environ.get("MAILGUN_DOMAIN")
    MAILGUN_API_KEY = os.environ.get("MAILGUN_API_KEY")
    FROM_EMAIL = "postmaster@sandboxd1b9447d2f3247ea842d74f59c675f36.mailgun.org"
    TITLE = "signup email"

    @classmethod
    def send_email(
        cls, email: List[str], subject: str, message_body: str, html: str
    ) -> Response:
        if cls.MAILGUN_API_KEY is None or cls.MAILGUN_DOMAIN is None:
            raise MailGunException("No MAILGUN_API_KEY set.")
        if cls.MAILGUN_DOMAIN is None:
            raise MailGunException("No MAILGUN_DOMAIN set.")

        return requests.post(
            f"https://api.mailgun.net/v3/{cls.MAILGUN_DOMAIN}/messages",
            auth=("api", cls.MAILGUN_API_KEY),
            data={
                "from": f"{cls.TITLE} <mailgun@{cls.MAILGUN_DOMAIN}>",
                "to": [email],
                "subject": subject,
                "text": f"Please click the link {message_body}",
                "html": html,
            },
        )
