from rest_framework import serializers

from api.models import User, Project, Contributor


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "email", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create(
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            email=validated_data["email"]
            )
        user.set_password(validated_data["password"])
        user.save()
        return user


class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = ["id", "author_id", "title", "description", "type"]


class ContributorSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField(source="user.id", read_only=True)
    first_name = serializers.CharField(source="user.first_name", read_only=True)
    last_name = serializers.CharField(source="user.last_name", read_only=True)
    email = serializers.CharField(source="user.email", read_only=True)

    class Meta:
        model = Contributor
        fields = ["user", "id", "first_name", "last_name", "email"]
        extra_kwargs = {"user": {"write_only": True}}
