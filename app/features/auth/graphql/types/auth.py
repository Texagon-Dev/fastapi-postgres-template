import strawberry
from .user import UserType

@strawberry.type
class AuthPayload:
    access_token: str
    token_type: str
    user: UserType

@strawberry.input
class LoginInput:
    email: str
    password: str