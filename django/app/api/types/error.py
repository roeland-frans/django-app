import graphene

from app.utils.camel_case import to_camel_case


class InputFieldError(graphene.ObjectType):
    name = graphene.String(
        required=True,
        description=(
            "The field name of the input object that this error applies to."
        ),
    )
    message = graphene.String(
        required=True,
        description="The error message associated with the input field.",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = to_camel_case(self.name)

    def __eq__(self, other):
        return self.name == other.name and self.message == other.message


class InputErrorType(graphene.ObjectType):
    """
    This is returned by a mutation whenever there are one or more input
    object fields that contain validation errors.
    """

    message = graphene.String(
        description="General error message for the whole mutation."
    )
    field_errors = graphene.List(
        InputFieldError,
        description="A list of errors related to the input object fields.",
    )
