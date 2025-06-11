import strawberry
from app.features.auth.graphql.queries.user import UserQuery
from app.features.auth.graphql.mutations.auth import AuthMutation

@strawberry.type
class Query(
    UserQuery, 
    ):
    pass

@strawberry.type
class Mutation(AuthMutation):
    pass

schema = strawberry.Schema(query=Query, mutation=Mutation)