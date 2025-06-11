import strawberry
from typing import List, Optional
from ..types.user import UserType, UserPermissions
from app.models.user import User as UserModel
from sqlalchemy.orm import Session
from app.features.auth.service import get_user_permissions_service
from app.utils.permissions import Permission, require_auth

@strawberry.type
class UserQuery:
    @strawberry.field
    @require_auth(Permission.VIEW_ALL_USERS)
    def users(self, info) -> List[UserType]:
        db: Session = info.context["db"]
        
        db_users = db.query(UserModel).all()
        return [
            UserType(
                id=str(user.id),
                first_name=user.first_name,
                last_name=user.last_name,
                email=user.email,
                role=user.role.value,
                is_active=user.is_active,
                created_at=user.created_at
            )
            for user in db_users
        ]
    
    @strawberry.field
    @require_auth()
    def user(self, info, id: strawberry.ID) -> Optional[UserType]:
        db: Session = info.context["db"]
        
        db_user = db.query(UserModel).filter(UserModel.id == id).first()
        if not db_user:
            return None
            
        return UserType(
            id=str(db_user.id),
            first_name=db_user.first_name,
            last_name=db_user.last_name,
            email=db_user.email,
            role=db_user.role.value,
            is_active=db_user.is_active,
            created_at=db_user.created_at
        )
    
    @strawberry.field
    @require_auth()
    def me(self, info) -> Optional[UserType]:
        current_user = info.context.get("current_user")
            
        return UserType(
            id=str(current_user.id),
            first_name=current_user.first_name,
            last_name=current_user.last_name,
            email=current_user.email,
            role=current_user.role.value,
            is_active=current_user.is_active,
            created_at=current_user.created_at
        )
    
    @strawberry.field
    @require_auth()
    def my_permissions(self, info: strawberry.Info) -> UserPermissions:
        current_user = info.context.get("current_user")
        permissions = get_user_permissions_service(current_user)
        return UserPermissions(
            user_id=str(current_user.id),
            role=current_user.role.value,
            permissions=permissions
        )