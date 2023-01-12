from rest_framework import generics, permissions

from .models import Note, Tag
from .serializers import NoteSerializer, TagSerializer


class NoteList(generics.ListCreateAPIView):
    # TODO: Add filtering against tags here
    # See: https://www.django-rest-framework.org/api-guide/filtering/#filtering-against-query-parameters # noqa: E501
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class NoteDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class TagList(generics.ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
