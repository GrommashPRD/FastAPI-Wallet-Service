from fastapi import Response, APIRouter, HTTPException

from app.api.handlers.auth import schemas
from app.usecase.auth import usecase
from app.usecase.auth import exceptions as auth_exceptions

from app.logger import logger

router = APIRouter()


@router.post("/login/")
async def login_user(
        response: Response,
        user_data: schemas.SUserAuthData
):
    """
    User Log In endpoint.
    :param response: User response.
    :param user_data: username: str и password: str.
    :return: message и user_id.
    """
    try:
        user = await usecase.login(response, user_data)
    except auth_exceptions.UserNotFound as e:
        logger.warning("User not found %s", e)
        raise HTTPException(detail="Username not found", status_code=400)
    except auth_exceptions.WrongPassword:
        logger.warning("Incorrect password")
        raise HTTPException(detail="Incorrect password", status_code=400)

    return {
        "message": "OK",
        "user_id": user.id
    }
