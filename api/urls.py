from django.urls import path, include

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from api import views

urlpatterns = [

    # Authentication
    path("api-auth/", include("rest_framework.urls")),
    path("signup/", views.SignupView.as_view()),
    path("token/", TokenObtainPairView.as_view()),
    path("token/refresh/", TokenRefreshView.as_view()),

    # Projects
    path("projects/", views.ProjectListCreate.as_view()),
    path("projects/<int:project_id>/", views.ProjectRetrieveUpdateDestroy.as_view()),

    # Contributors
    path("projects/<int:project_id>/users/", views.ContributorList.as_view()),
    path("projects/<int:project_id>/users/<int:user_id>/", views.contributor_create_destroy),

    # Issues
    path("projects/<int:project_id>/issues/", views.IssueListCreate.as_view()),
    path("projects/<int:project_id>/issues/<int:issue_id>/", views.IssueRetrieveUpdateDestroy.as_view()),

    # Comments
    path("projects/<int:project_id>/issues/<int:issue_id>/comments/", views.CommentListCreate.as_view()),
    path("projects/<int:project_id>/issues/<int:issue_id>/comments/<int:comment_id>/",
         views.CommentRetrieveUpdateDestroy.as_view()),

]
