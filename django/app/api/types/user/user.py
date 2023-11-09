import graphene

from app.models.user import User
from graphene_django import DjangoObjectType


class UserType(DjangoObjectType):
    """
    This object is the entry point for all queryable objects linked to the
    authenticated user.
    """

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "phone_number",
            "first_name",
            "last_name",
            "full_name",
            "date_joined",
        )

    full_name = graphene.String(
        description="The user's full name i.e. `first_name` + `last_name`."
    )
    date_joined = graphene.DateTime(description="The date the user signed up.")
