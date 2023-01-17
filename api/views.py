from django.shortcuts import get_object_or_404
from django.db import IntegrityError

from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import PermissionDenied, ParseError
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from api.models import User, Project, Contributor, Issue, Comment
from api.serializers import (
    UserSerializer,
    ProjectSerializer,
    ContributorSerializer,
    IssueListCreateSerializer, IssueRetrieveUpdateDestroySerializer,
    CommentSerializer
    )
from api.helpers import (
    check_project_contributor_access,
    check_project_author_access,
    check_issue_author_access,
    check_comment_author_access
)


class SignupView(generics.ListCreateAPIView):

    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]


class ProjectListCreate(generics.ListCreateAPIView):

    serializer_class = ProjectSerializer

    def perform_create(self, serializer):
        project = serializer.save(author=self.request.user)
        contributor = Contributor(user=self.request.user, project=project)
        contributor.save()

    def get_queryset(self):
        user_contributors = Contributor.objects.filter(user=self.request.user)
        return Project.objects.filter(contributors__in=user_contributors)


class ProjectRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = ProjectSerializer
    lookup_url_kwarg = "project_id"

    def perform_update(self, serializer):
        check_project_author_access(self.kwargs["project_id"], self.request.user)
        if serializer.is_valid():
            serializer.save()

    def perform_destroy(self, instance):
        check_project_author_access(self.kwargs["project_id"], self.request.user)
        instance.delete()

    def get_queryset(self):
        check_project_contributor_access(self.kwargs["project_id"], self.request.user)
        return Project.objects.filter(pk=self.kwargs["project_id"])


class ContributorList(generics.ListAPIView):

    serializer_class = ContributorSerializer

    def get_queryset(self):
        check_project_contributor_access(self.kwargs["project_id"], self.request.user)
        return Contributor.objects.filter(project__pk=self.kwargs["project_id"])


@api_view(["POST", "DELETE"])
def contributor_create_destroy(request, project_id, user_id):

    project = get_object_or_404(Project, pk=project_id)
    user = get_object_or_404(User, pk=user_id)
    check_project_author_access(project.pk, request.user)

    if request.method == "POST":
        contributor = Contributor()
        contributor.user = user
        contributor.project = project
        try:
            contributor.save()
        except IntegrityError:
            raise ParseError("Opération annulée. Cet utilisateur est déjà un contributeur de ce projet.")
        return Response(status=status.HTTP_201_CREATED)

    if request.method == "DELETE":
        if request.user == user:
            raise ParseError("Opération annulée. Il est impossible de retirer l'auteur de la liste des contributeurs.")
        contributor = get_object_or_404(Contributor, user=user, project=project)
        contributor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class IssueListCreate(generics.ListCreateAPIView):

    serializer_class = IssueListCreateSerializer

    def perform_create(self, serializer):
        project = get_object_or_404(Project, pk=self.kwargs["project_id"])
        serializer.save(author=self.request.user, user_in_charge=self.request.user, project=project)

    def get_queryset(self):
        check_project_contributor_access(self.kwargs["project_id"], self.request.user)
        return Issue.objects.filter(project__pk=self.kwargs["project_id"])


class IssueRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = IssueRetrieveUpdateDestroySerializer
    lookup_url_kwarg = "issue_id"

    def perform_update(self, serializer):
        check_issue_author_access(self.kwargs["issue_id"], self.request.user)
        project = get_object_or_404(Project, pk=self.kwargs["project_id"])
        if serializer.is_valid():
            user_in_charge = serializer.validated_data["user_in_charge"]
            user_in_charge_contributors = Contributor.objects.filter(user=user_in_charge)
            if len(Project.objects.filter(pk=project.pk, contributors__in=user_in_charge_contributors)) == 0:
                raise PermissionDenied(
                    "Opération annulée. Vous ne pouvez pas assigner un problème à un utilisateur " +
                    "qui n'est pas un contributeur de ce projet.")
            serializer.save()

    def perform_destroy(self, instance):
        check_issue_author_access(self.kwargs["issue_id"], self.request.user)
        instance.delete()

    def get_queryset(self):
        check_project_contributor_access(self.kwargs["project_id"], self.request.user)
        return Issue.objects.filter(project__pk=self.kwargs["project_id"])


class CommentListCreate(generics.ListCreateAPIView):

    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        issue = get_object_or_404(Issue, pk=self.kwargs["issue_id"])
        serializer.save(author=self.request.user, issue=issue)

    def get_queryset(self):
        check_project_contributor_access(self.kwargs["project_id"], self.request.user)
        issue = get_object_or_404(Issue, pk=self.kwargs["issue_id"])
        return Comment.objects.filter(issue=issue)


class CommentRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = CommentSerializer
    lookup_url_kwarg = "comment_id"

    def perform_update(self, serializer):
        check_comment_author_access(self.kwargs["comment_id"], self.request.user)
        if serializer.is_valid():
            serializer.save()

    def perform_destroy(self, instance):
        check_comment_author_access(self.kwargs["comment_id"], self.request.user)
        instance.delete()

    def get_queryset(self):
        check_project_contributor_access(self.kwargs["project_id"], self.request.user)
        return Comment.objects.filter(pk=self.kwargs["comment_id"])
