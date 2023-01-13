from rest_framework import serializers

from api.models import User, Project


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "email", "username", "password"]

    def create(self, validated_data):
        user = User.objects.create(
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            username=validated_data["username"],
            email=validated_data["email"]
            )
        user.set_password(validated_data["password"])
        user.save()
        return user


class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = ["id", "author_id", "title", "description", "type"]
        read_only_fields = ["author_id"]
