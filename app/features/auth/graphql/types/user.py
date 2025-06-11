import strawberry
from typing import Optional, List
from datetime import datetime

@strawberry.type
class UserType:
    id: strawberry.ID
    first_name: str
    last_name: str
    email: str
    role: str
    is_active: bool
    created_at: datetime
    
    @strawberry.field
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"
    @classmethod
    def from_model(cls, user_model):
        return cls(
            id=str(user_model.id),
            first_name=user_model.first_name,
            last_name=user_model.last_name,
            email=user_model.email,
            role=user_model.role,
            is_active=user_model.is_active,
            created_at=user_model.created_at
        )

@strawberry.input
class UserCreateInput:
    first_name: str
    last_name: str
    email: str
    role: str
    password: str
    confirm_password: str
    is_active: Optional[bool] = True

@strawberry.input
class UserUpdateInput:
    id: strawberry.ID
    first_name: Optional[str] = strawberry.UNSET
    last_name: Optional[str] = strawberry.UNSET
    email: Optional[str] = strawberry.UNSET
    role: Optional[str] = strawberry.UNSET
    is_active: Optional[bool] = strawberry.UNSET

@strawberry.input
class ChangePasswordInput:
    old_password: str
    new_password: str
    confirm_password: str

@strawberry.type
class UserPermissions:
    user_id: strawberry.ID
    role: str
    permissions: List[str]