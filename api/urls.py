from django.urls import path, include

from api import views

urlpatterns = [
    path("api-auth/", include("rest_framework.urls")),
    path("signup/", views.SignupView.as_view()),
    path("projects/", views.ProjectListCreate.as_view()),
    path("projects/<int:project_id>/", views.ProjectRetrieveUpdateDestroy.as_view()),
    path("projects/<int:project_id>/users/", views.ContributorList.as_view()),
    path("projects/<int:project_id>/users/<int:user_id>/", views.contributor_create_destroy),
    path("projects/<int:project_id>/issues/", views.IssueListCreate.as_view()),
    path("projects/<int:project_id>/issues/<int:issue_id>/", views.IssueRetrieveUpdateDestroy.as_view()),
]
