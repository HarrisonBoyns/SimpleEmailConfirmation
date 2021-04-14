from flask import jsonify
from app.resources.user_resource import revoked_tokens

INVALID_TOKEN = "Invalid token"
EXPIRED_TOKEN = "Expired token"
EXPIRED_TOKEN_ERROR = "token_expired"
NO_TOKEN = "No token"
FRESH_TOKEN = "fresh token required"
REFRESH_TOKEN_ERROR = "fresh_token_needed"
REVOKED_TOKEN = "The token has been revoked"
REVOKED_TOKEN_ERROR = "token not valid"


def register_callbacks(jwt_manager):
    @jwt_manager.token_in_blocklist_loader
    def is_in_blacklist(jwt_header, jwt_payload):
        return jwt_payload["jti"] in revoked_tokens

    @jwt_manager.expired_token_loader
    def expired_token_callback(jwt_header, jwt_data):
        return {"description": EXPIRED_TOKEN, "error": EXPIRED_TOKEN_ERROR}, 401

    @jwt_manager.invalid_token_loader
    def invalid_token_callback(error):
        return {"description": INVALID_TOKEN, "error": error}, 401

    @jwt_manager.unauthorized_loader
    def unauthorised_loader(error):
        return {"description": NO_TOKEN, "error": error}, 401

    @jwt_manager.needs_fresh_token_loader
    def refresh_token_callback(jwt_header, jwt_data):
        return (
            jsonify({"description": FRESH_TOKEN, "error": REFRESH_TOKEN_ERROR}),
            401,
        )

    @jwt_manager.revoked_token_loader
    def revoked_token_callback():
        return (
            jsonify(
                {
                    "description": REVOKED_TOKEN,
                    "error": REVOKED_TOKEN_ERROR,
                }
            ),
            401,
        )
