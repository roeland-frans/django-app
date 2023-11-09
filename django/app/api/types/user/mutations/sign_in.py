import graphene

from app.models.user import User
from email_validator import ValidatedEmail
from email_validator import validate_email
from graphql_jwt.decorators import token_auth
from graphql_jwt.mixins import ObtainJSONWebTokenMixin
from graphql_jwt.mixins import ResolveMixin


class SignInInput(graphene.InputObjectType):
    """
    Specifies the information to sign a user in.
    """

    email = graphene.String(
        required=True, description="The user's email address."
    )
    password = graphene.String(
        required=True, description="The user's password."
    )


class SignInMutation(ResolveMixin, ObtainJSONWebTokenMixin, graphene.Mutation):
    """
    This mutation will authenticate the given user email and password. Once
    authenticated the mutation will return the JWT token and refresh token to
    be able to refresh the JWT token. This mutation will also set the two
    secure cookies containing the JWT token and the refresh token.

    This is useful for browsers to open an authenticated user session where
    all subsequent fetch calls will be authenticated by the cookies.
    """

    class Arguments:
        input = graphene.Argument(SignInInput, required=True)

    id = graphene.ID(description="The user's ID.")
    email = graphene.String(description="The user's email address.")
    first_name = graphene.String(description="The user's first name.")
    last_name = graphene.String(description="The user's last name.")
    full_name = graphene.String(description="The user's full name.")

    @classmethod
    def mutate(cls, root, info, input: SignInInput):
        validated_email: ValidatedEmail = validate_email(input.email)
        auth = cls.auth(
            root, info, email=validated_email.email, password=input.password
        )
        user: User = info.context.user
        auth.id = user.id
        auth.email = user.email
        auth.first_name = user.first_name
        auth.last_name = user.last_name
        auth.full_name = user.full_name
        return auth

    @classmethod
    @token_auth
    def auth(cls, root, info, **kwargs):
        return cls.resolve(root, info, **kwargs)
