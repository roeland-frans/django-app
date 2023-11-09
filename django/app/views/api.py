from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView


class ApiView(GraphQLView):
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        if request.method.lower() == "options":
            response = HttpResponse()
            response["allow"] = "get, post"
            return response
        return super().dispatch(request, *args, **kwargs)


class GraphiQLView(LoginRequiredMixin, GraphQLView):
    pass
