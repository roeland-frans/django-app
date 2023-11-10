import graphene

from graphql import GraphQLResolveInfo
from graphql_jwt.mixins import DeleteJSONWebTokenCookieMixin
from graphql_jwt.refresh_token.mixins import DeleteRefreshTokenCookieMixin


class SignOutMutation(graphene.Mutation):
    """
    This mutation will sign the current user out. Signing a user out means that
    that their JWT cookies get deleted and they no longer can make authenticated
    API requests.
    """

    deleted = graphene.Boolean(
        required=True,
        description=(
            "Confirms whether both the JWT and refresh tokens were deleted."
        ),
    )
    signed_out = graphene.Boolean(required=True)

    class DeleteJwtToken(graphene.ObjectType, DeleteJSONWebTokenCookieMixin):
        pass

    class DeleteRefreshToken(
        graphene.ObjectType, DeleteRefreshTokenCookieMixin
    ):
        pass

    @classmethod
    def mutate(cls, root: None, info: GraphQLResolveInfo):
        delete_jwt_token = cls.DeleteJwtToken.delete_cookie(root, info)
        delete_refresh_token = cls.DeleteRefreshToken.delete_cookie(root, info)
        return cls(
            deleted=(
                delete_jwt_token.deleted and delete_refresh_token.deleted
            ),
            signed_out=True,
        )
