from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from .views import NoteDetail, NoteList, TagList

urlpatterns = [
    path('notes/', NoteList.as_view(), name="notes"),
    path('note/<int:pk>', NoteDetail.as_view(), name="note"),
    path('tags/', TagList.as_view(), name="tags"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
