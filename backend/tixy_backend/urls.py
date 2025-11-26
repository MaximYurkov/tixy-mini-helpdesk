from django.contrib import admin
from django.urls import path
from issues.views import health
from strawberry.django.views import GraphQLView
from .schema import schema
from django.views.decorators.csrf import csrf_exempt  
from issues import views as issue_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/health", health),
    path("graphql", csrf_exempt(GraphQLView.as_view(schema=schema))),
    path("api/tasks/cat-fact/", issue_views.create_cat_fact_task),
    path("api/tasks/<str:task_id>/", issue_views.get_task_status),  
]
