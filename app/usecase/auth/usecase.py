from app.api.handlers.auth.schemas import SUserAuthData
from app.repository.users.repo import UsersRepo
from sqlalchemy.ext.asyncio import AsyncSession
from app.auth import auth
from app.repository import exceptions as repository_exceptions
from app.usecase.auth import exceptions as auth_exceptions


async def registration(
        session: AsyncSession,
        registration_data: SUserAuthData,
):
    hashed_password = auth.hash_password(registration_data.password)

    try:
        user = await UsersRepo.add_new(
            session,
            check_conditions={"username": registration_data.username},
            username=registration_data.username,
            password=hashed_password
        )
    except repository_exceptions.RecordAlreadyExist:
        raise auth_exceptions.UserAlreadyExist(detail="Username already exist")

    session.add(user)
    await session.commit()

    return user


async def login(
        response,
        login_data: SUserAuthData
):
    user = await UsersRepo.find_one_or_none(username=login_data.username)

    if not user:
        raise auth_exceptions.UserNotFound(detail=login_data.username)
    elif not auth.verify_password(login_data.password, user.password):
        raise auth_exceptions.WrongPassword(detail="Incorrect password")

    access_token = auth.create_access_token({"sub": str(user.id)})

    response.set_cookie(
        "access_token",
        access_token,
        httponly=True,
    )

    return user
