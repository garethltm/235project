from werkzeug.security import generate_password_hash, check_password_hash

from games.adapters.repository import AbstractRepository
from games.domainmodel.model import User


class NameNotUniqueException(Exception):
    pass


class UnknownUserException(Exception):
    pass


class AuthenticationException(Exception):
    pass


def addUser(username: str, password: str, repo: AbstractRepository):
    user = repo.getUser(username)
    if user is not None:
        raise NameNotUniqueException

    password_hash = generate_password_hash(password)
    user = User(username, password_hash)
    repo.addUser(user)


def getUser(username: str, repo: AbstractRepository):
    user = repo.getUser(username)
    if user is None:
        raise UnknownUserException
    return userToDict(user)


def authUser(username: str, password: str, repo: AbstractRepository):
    authenticated = False
    user = repo.getUser(username)
    if user is not None:
        authenticated = check_password_hash(user.password, password)
    if not authenticated:
        raise AuthenticationException
    return authenticated


def userToDict(user: User):
    user_dict = {
        'user_name': user.username,
        'password': user.password
    }
    return user_dict