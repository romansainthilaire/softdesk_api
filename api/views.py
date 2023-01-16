from django.shortcuts import get_object_or_404
from django.db import IntegrityError

from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import PermissionDenied, ParseError
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from api.models import User, Project, Contributor
from api.serializers import (
    UserSerializer,
    ProjectSerializer,
    ContributorSerializer,
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

    def get_queryset(self):
        project = get_object_or_404(Project, pk=self.kwargs["pk"])
        if self.request.user != project.author:
            raise PermissionDenied("Access denied. You are not the author of this project.")
        return Project.objects.filter(author=self.request.user)


class ContributorListCreate(generics.ListCreateAPIView):

    serializer_class = ContributorSerializer

    def perform_create(self, serializer):
        project = get_object_or_404(Project, pk=self.kwargs["pk"])
        if self.request.user != project.author:
            raise PermissionDenied("Access denied. You are not the author of this project.")
        try:
            serializer.save(project=project)
        except IntegrityError:
            raise ParseError("Operation canceled. This user is already a contributor to this project.")

    def get_queryset(self):
        project = get_object_or_404(Project, pk=self.kwargs["pk"])
        if self.request.user != project.author:
            raise PermissionDenied("Access denied. You are not the author of this project.")
        return Contributor.objects.filter(project=project)


@api_view(["DELETE"])
def delete_contributor(request, project_id, user_id):

    project = get_object_or_404(Project, pk=project_id)
    if request.user != project.author:
        raise PermissionDenied("Access denied. You are not the author of this project.")

    user = get_object_or_404(User, pk=user_id)
    if request.user == user:
        raise ParseError("Operation canceled. You cannot remove the author from the contributors.")

    if request.method == "DELETE":
        contributor = get_object_or_404(Contributor, user=user, project=project)
        contributor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
