from rest_framework import generics, permissions

from .models import Note, Tag
from .serializers import NoteSerializer, TagSerializer


class NoteList(generics.ListCreateAPIView):
    # TODO: Add filtering against tags here
    # See: https://www.django-rest-framework.org/api-guide/filtering/#filtering-against-query-parameters # noqa: E501
    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):

        queryset = Note.objects.all()
        if tag_name := self.request.query_params.get('tag'):
            queryset = queryset.filter(tags__name=tag_name)

        return queryset


class NoteDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class TagList(generics.ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
