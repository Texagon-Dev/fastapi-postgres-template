import strawberry
from app.features.auth.graphql.types.auth import AuthPayload, LoginInput
from app.features.auth.graphql.types.user import UserType, UserCreateInput, UserUpdateInput, ChangePasswordInput
from app.features.auth.service import login_service, create_user_service, update_user_service, change_password_service
from sqlalchemy.orm import Session
import uuid
from app.utils.permissions import require_auth, Permission
import logging
logger = logging.getLogger(__name__)

@strawberry.type
class AuthMutation:
    @strawberry.mutation
    def login(self, info, input: LoginInput) -> AuthPayload:
        db: Session = info.context["db"]
        
        token_response = login_service(db, input.email, input.password)
        
        from app.models.user import User as UserModel
        db_user = db.query(UserModel).filter(UserModel.email == input.email).first()
        
        user = UserType(
            id=str(db_user.id),
            first_name=db_user.first_name,
            last_name=db_user.last_name,
            email=db_user.email,
            role=db_user.role.value,
            is_active=db_user.is_active,
            created_at=db_user.created_at
        )
        
        return AuthPayload(
            access_token=token_response.access_token,
            token_type=token_response.token_type,
            user=user
        )
    
    @strawberry.mutation
    @require_auth(Permission.CREATE_USER)
    def create_user(self, info, input: UserCreateInput) -> UserType:
        db: Session = info.context["db"]

        db_user = create_user_service(db, input)
        
        return UserType(
            id=str(db_user.id),
            first_name=db_user.first_name,
            last_name=db_user.last_name,
            email=db_user.email,
            role=db_user.role.value,
            is_active=db_user.is_active,
            created_at=db_user.created_at
        )
    
    @strawberry.mutation
    @require_auth()
    def update_user(self, info, input: UserUpdateInput) -> UserType:
        db: Session = info.context["db"]
        current_user = info.context.get("current_user")
        
        if not current_user:
            raise Exception("Authentication required")
        
        update_data = {}
        if input.first_name is not strawberry.UNSET:
            update_data['first_name'] = input.first_name
        if input.last_name is not strawberry.UNSET:
            update_data['last_name'] = input.last_name
        if input.email is not strawberry.UNSET:
            update_data['email'] = input.email
        if input.role is not strawberry.UNSET:
            update_data['role'] = input.role
        if input.is_active is not strawberry.UNSET:
            update_data['is_active'] = input.is_active
        
        try:
            updated_user = update_user_service(
                db=db, 
                current_user=current_user, 
                user_id=uuid.UUID(input.id), 
                update_data=update_data
            )
            
            return UserType(
                id=str(updated_user.id),
                first_name=updated_user.first_name,
                last_name=updated_user.last_name,
                email=updated_user.email,
                role=updated_user.role.value,
                is_active=updated_user.is_active,
                created_at=updated_user.created_at
            )
        except ValueError as e:
            logger.error(f"Error updating user: {str(e)}")
            raise Exception(str(e))
        
    @strawberry.mutation
    @require_auth()
    def change_password(self, info, input: ChangePasswordInput) -> UserType:
        db: Session = info.context["db"]
        current_user = info.context.get("current_user")

        try:
            updated_user = change_password_service(
                db=db,
                current_user=current_user,
                old_password=input.old_password,
                new_password=input.new_password
            )

            return UserType(
                id=str(updated_user.id),
                first_name=updated_user.first_name,
                last_name=updated_user.last_name,
                email=updated_user.email,
                role=updated_user.role.value,
                is_active=updated_user.is_active,
                created_at=updated_user.created_at
            )
        except ValueError as e:
            logger.error(f"Error changing password: {str(e)}")
            raise Exception(str(e))