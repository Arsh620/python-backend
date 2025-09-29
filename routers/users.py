from fastapi import APIRouter
from typing import List
from schemas import UserResponse
from controllers.user_controller import get_current_user_info, get_users, get_user, update_user_info, delete_user_account

router = APIRouter(prefix="/users", tags=["users"])

router.add_api_route("/me", get_current_user_info, methods=["GET"], response_model=UserResponse)
router.add_api_route("", get_users, methods=["GET"], response_model=List[UserResponse])
router.add_api_route("/{user_id}", get_user, methods=["GET"], response_model=UserResponse)
router.add_api_route("/{user_id}", update_user_info, methods=["PUT"], response_model=UserResponse)
router.add_api_route("/{user_id}", delete_user_account, methods=["DELETE"])