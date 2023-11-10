import graphene

from app.api.types.error import InputErrorType
from app.api.types.error import InputFieldError
from app.api.types.user.user import UserType
from app.models.user import User
from django.utils.translation import gettext_lazy as _
from email_validator import EmailNotValidError
from email_validator import validate_email
from graphql import GraphQLResolveInfo
from graphql_jwt.decorators import login_required


class UpdateUserInput(graphene.InputObjectType):
    """
    Specifies the information to be updated for the given user.
    """

    id = graphene.ID(
        required=True,
        description="The user's ID as returned by the UserType object.",
    )
    email = graphene.String(
        description=(
            "A valid email address. An error will be returned if the email is "
            "invalid."
        )
    )
    phone_number = graphene.String(description="The user's phone number.")
    first_name = graphene.String(description="The user's first name.")
    last_name = graphene.String(description="The user's last name.")


class UpdateUserResultType(graphene.Union):
    """
    Returns either the user object containing the updated fields, or it
    returns and input error object containing a list of field errors.
    """

    class Meta:
        types = (UserType, InputErrorType)


class UpdateUserMutation(graphene.Mutation):
    """
    This mutation allows a user's information to be updated. If a user's email
    address is changed, a verification email will be sent to the new email
    address. The user will first need to confirm the new email address with
    the given confirmation URL before their old email address is replaced with
    the new email address. All email confirmation URLs expire after a couple of
    hours.
    """

    class Arguments:
        input = graphene.Argument(UpdateUserInput, required=True)

    user_or_error = graphene.Field(UpdateUserResultType)

    @classmethod
    @login_required
    def mutate(
        cls, root: None, info: GraphQLResolveInfo, input: UpdateUserInput
    ):
        field_errors = []

        user = User.objects.get(id=input.id)
        if input.email:
            try:
                validated_email = validate_email(input.email)
                user.email = validated_email.normalized
            except EmailNotValidError:
                field_errors.append(
                    InputFieldError(
                        name="email", message=_("Invalid email address.")
                    )
                )
        if input.phone_number:
            user.phone_number = input.phone_number
        if input.first_name:
            user.first_name = input.first_name
        if input.last_name:
            user.last_name = input.last_name

        if field_errors:
            return cls(
                user_or_error=InputErrorType(
                    message=_(
                        "Could not update the user, some input fields contain "
                        "errors."
                    ),
                    field_errors=field_errors,
                )
            )
        else:
            user.save()
            return cls(user_or_error=user)
