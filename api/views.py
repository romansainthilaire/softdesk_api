from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

from rest_framework import generics
from rest_framework.permissions import AllowAny

from api.models import User, Project
from api.serializers import UserSerializer, ProjectSerializer


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
            raise PermissionDenied()
        return Project.objects.filter(author=self.request.user)
