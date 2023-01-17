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


class SignupView(generics.CreateAPIView):

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
        project = get_object_or_404(Project, pk=self.kwargs["project_id"])
        if self.request.user != project.author:
            raise PermissionDenied("Opération annulée. Vous n'êtes pas l'auteur de ce projet.")
        if serializer.is_valid():
            serializer.save()

    def perform_destroy(self, instance):
        if self.request.user != instance.author:
            raise PermissionDenied("Opération annulée. Vous n'êtes pas l'auteur de ce projet.")
        instance.delete()

    def get_queryset(self):
        project = get_object_or_404(Project, pk=self.kwargs["project_id"])
        user_contributors = Contributor.objects.filter(user=self.request.user)
        if len(Project.objects.filter(pk=project.pk, contributors__in=user_contributors)) == 0:
            raise PermissionDenied("Accès refusé. Vous n'êtes pas un contributeur de ce projet.")
        return Project.objects.all()


class ContributorList(generics.ListAPIView):

    serializer_class = ContributorSerializer

    def get_queryset(self):
        project = get_object_or_404(Project, pk=self.kwargs["project_id"])
        user_contributors = Contributor.objects.filter(user=self.request.user)
        if len(Project.objects.filter(pk=project.pk, contributors__in=user_contributors)) == 0:
            raise PermissionDenied("Accès refusé. Vous n'êtes pas un contributeur de ce projet.")
        return Contributor.objects.filter(project=project)


@api_view(["POST", "DELETE"])
def contributor_create_destroy(request, project_id, user_id):

    project = get_object_or_404(Project, pk=project_id)
    if request.user != project.author:
        raise PermissionDenied("Accès refusé. Vous n'êtes pas l'auteur de ce projet.")

    user = get_object_or_404(User, pk=user_id)

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
        project = get_object_or_404(Project, pk=self.kwargs["project_id"])
        user_contributors = Contributor.objects.filter(user=self.request.user)
        if len(Project.objects.filter(pk=project.pk, contributors__in=user_contributors)) == 0:
            raise PermissionDenied("Accès refusé. Vous n'êtes pas un contributeur de ce projet.")
        return Issue.objects.filter(project=project)


class IssueRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = IssueRetrieveUpdateDestroySerializer
    lookup_url_kwarg = "issue_id"

    def perform_update(self, serializer):
        issue = get_object_or_404(Issue, pk=self.kwargs["issue_id"])
        if self.request.user != issue.author:
            raise PermissionDenied("Opération annulée. Vous n'êtes pas l'auteur de ce problème.")
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
        if self.request.user != instance.author:
            raise PermissionDenied("Opération annulée. Vous n'êtes pas l'auteur de ce problème.")
        instance.delete()

    def get_queryset(self):
        project = get_object_or_404(Project, pk=self.kwargs["project_id"])
        user_contributors = Contributor.objects.filter(user=self.request.user)
        if len(Project.objects.filter(pk=project.pk, contributors__in=user_contributors)) == 0:
            raise PermissionDenied("Accès refusé. Vous n'êtes pas un contributeur de ce projet.")
        return Issue.objects.filter(project=project)


class CommentListCreate(generics.ListCreateAPIView):

    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        issue = get_object_or_404(Issue, pk=self.kwargs["issue_id"])
        serializer.save(author=self.request.user, issue=issue)

    def get_queryset(self):
        project = get_object_or_404(Project, pk=self.kwargs["project_id"])
        user_contributors = Contributor.objects.filter(user=self.request.user)
        if len(Project.objects.filter(pk=project.pk, contributors__in=user_contributors)) == 0:
            raise PermissionDenied("Accès refusé. Vous n'êtes pas un contributeur de ce projet.")
        issue = get_object_or_404(Issue, pk=self.kwargs["issue_id"])
        return Comment.objects.filter(issue=issue)
