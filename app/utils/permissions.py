from enum import Enum
from typing import List, Optional, Any, Callable
from app.models.user import User, UserRole
from sqlalchemy.orm import Session
from functools import wraps
import strawberry

class Permission(Enum):
    # User permissions
    VIEW_ALL_USERS = "view_all_users"
    CREATE_USER = "create_user"
    UPDATE_USER = "update_user"
    DELETE_USER = "delete_user"
    VIEW_OWN_PROFILE = "view_own_profile"
    

ROLE_PERMISSIONS = {
    UserRole.ADMIN: [
        # Users
        Permission.VIEW_ALL_USERS,
        Permission.CREATE_USER,
        Permission.UPDATE_USER,
        Permission.DELETE_USER,
        Permission.VIEW_OWN_PROFILE
    ],
    
    UserRole.MANAGER: [
        # Users
        Permission.VIEW_OWN_PROFILE,
        Permission.CREATE_USER
    ],
    
    UserRole.EMPLOYEE: [
        Permission.VIEW_OWN_PROFILE
    ]
}

def has_permission(user: User, permission: Permission) -> bool:
    if not user:
        return False
    
    user_permissions = ROLE_PERMISSIONS.get(user.role, [])
    return permission in user_permissions

def require_permission(permission: Permission):
    """Decorator to require specific permission for GraphQL resolvers"""
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(self, info: strawberry.Info, *args: Any, **kwargs: Any) -> Any:
            current_user = info.context.get("current_user")
            
            if not current_user:
                raise Exception("Authentication required")
            
            if not has_permission(current_user, permission):
                raise Exception(f"Insufficient permissions: {permission.value}")
            
            return func(self, info, *args, **kwargs)
        return wrapper
    return decorator

def require_auth(permission: Optional[Permission] = None):
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(self, info: strawberry.Info, *args: Any, **kwargs: Any) -> Any:
            current_user = info.context.get("current_user")
            
            if not current_user:
                raise strawberry.exceptions.StrawberryGraphQLError(
                    "Authentication required",
                    extensions={"code": "UNAUTHENTICATED"} 
                )

            if permission and not has_permission(current_user, permission):
                raise strawberry.exceptions.StrawberryGraphQLError(
                    f"Insufficient permissions: {permission.value}",
                    extensions={"code": "FORBIDDEN"}
                )
            
            return func(self, info, *args, **kwargs)
        return wrapper
    return decorator