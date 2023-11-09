import graphene

from django.conf import settings


class MetaType(graphene.ObjectType):
    app_version = graphene.String()

    @classmethod
    def resolve_versions(cls, parent, info) -> dict:
        return settings.VERSION
