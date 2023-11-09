import graphene

from app.api.types.meta import MetaType
from app.api.types.user.mutations.sign_in import SignInMutation
from app.api.types.user.user import UserType
from app.models.user import User
from graphql_jwt.decorators import login_required


class Query(graphene.ObjectType):
    meta = graphene.Field(MetaType)
    user = graphene.Field(UserType, required=True)

    @classmethod
    def resolve_meta(cls, parent: None, info) -> dict:
        return {}

    @classmethod
    @login_required
    def resolve_user(cls, parent: None, info) -> User:
        return info.context.user


class Mutation(graphene.ObjectType):
    sign_in = SignInMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
