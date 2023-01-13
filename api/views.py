from rest_framework import generics

from api.models import User, Project
from api.serializers import UserSerializer, ProjectSerializer


class SignupView(generics.CreateAPIView):

    serializer_class = UserSerializer
    queryset = User.objects.all()


class ProjectListCreate(generics.ListCreateAPIView):

    serializer_class = ProjectSerializer
    queryset = Project.objects.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
