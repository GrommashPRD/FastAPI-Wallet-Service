from fastapi import Request, Depends
from jose import jwt, JWTError

from app.config import settings
from datetime import datetime, timezone

from app.repository.users.repo import UsersRepo


def get_token(request: Request):
    token = request.cookies.get('access_token')
    return token


async def get_curr_user(token: str = Depends(get_token)):
    if token is None:
        return None

    try:
        payload = jwt.decode(
            token,
            key=settings.SECRET_KEY,
            algorithms=settings.ALGORITHM
        )
    except JWTError:
        return None

    expire: str = payload.get('exp')

    if not expire or (int(expire) < datetime.now(timezone.utc).timestamp()):
        return None

    user_id: str = payload.get('sub')
    if not user_id:
        return None

    user = await UsersRepo.find_by_id(str(user_id))
    if not user:
        return None

    return user


CurrentUserDep = Depends(get_curr_user)
