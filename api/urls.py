from django.urls import path, include

from api import views

urlpatterns = [
    path("api-auth/", include("rest_framework.urls")),
    path("signup/", views.SignupView.as_view()),
    path("projects/", views.ProjectListCreate.as_view()),
    path("projects/<int:pk>/", views.ProjectRetrieveUpdateDestroy.as_view()),
    path("projects/<int:pk>/users/", views.ContributorListCreate.as_view()),
    path("projects/<int:project_id>/users/<int:user_id>/", views.delete_contributor),
]
