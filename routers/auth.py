from fastapi import APIRouter, status, Request
from controllers.auth_controller import register, login

router = APIRouter(prefix="/auth", tags=["authentication"])

router.add_api_route("/register", register, methods=["POST"], status_code=status.HTTP_201_CREATED)
router.add_api_route("/login", login, methods=["POST"])