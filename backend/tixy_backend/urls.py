from django.contrib import admin
from django.urls import path
from issues.views import health
from strawberry.django.views import GraphQLView
from .schema import schema
from django.views.decorators.csrf import csrf_exempt  

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/health", health),
    path("graphql", csrf_exempt(GraphQLView.as_view(schema=schema))),  
]
