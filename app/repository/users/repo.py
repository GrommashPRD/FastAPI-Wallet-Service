from app.repository.base import BaseRepo
from app.repository.users.models import User


class UsersRepo(BaseRepo):
    model = User