from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Note, Tag


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = (
            "id",
            "name",
        )


class NoteSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, required=False)
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Note
        fields = ("id", "title", "body", "tags", "owner")
