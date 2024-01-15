"""
API Controller para `Profile`.
"""
from flask import Blueprint
from flask_jwt_extended import get_jwt_identity, jwt_required
from src.core.models.user import User
from src.web.schemas.users import user_schema


api_me_profile_blueprint = Blueprint("api_me_profile", __name__, url_prefix="/api/me")


@api_me_profile_blueprint.get("/profile")
@jwt_required()
def show():
    current_user = get_jwt_identity()
    user = User.find_by(id=current_user)
    return user_schema.dump(user), 200

