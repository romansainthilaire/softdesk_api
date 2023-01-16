from django.shortcuts import get_object_or_404
from django.db import IntegrityError

from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import PermissionDenied, ParseError

from api.models import User, Project, Contributor
from api.serializers import UserSerializer, ProjectSerializer, ContributorSerializer


class SignupView(generics.CreateAPIView):

    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]


class ProjectListCreate(generics.ListCreateAPIView):

    serializer_class = ProjectSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        return Project.objects.filter(author=self.request.user)


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
