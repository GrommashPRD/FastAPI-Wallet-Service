from fastapi import APIRouter, HTTPException
from app.database import async_session_maker
from app.usecase.auth import usecase
from app.api.handlers.auth.schemas import SUserAuthData
from app.usecase.auth import exceptions as auth_exceptions
from app.logger import logger

router = APIRouter()


@router.post("/register/")
async def register_user(
        registration_data: SUserAuthData
):
    """
    User registration endpoint.
    :param registration_data: username и password.
    :return: message и user_id.
    """
    async with async_session_maker() as session:
        try:
            registration = await usecase.registration(
                session,
                registration_data
            )
        except auth_exceptions.UserAlreadyExist:
            logger.warning(
                "Validation failed username - %s, password - %s",
                registration_data.username,
                registration_data.password
            )
            raise HTTPException(detail="User already exist", status_code=400)

        return {
            "message": "OK",
            "user_id": registration.id
        }
