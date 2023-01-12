from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from .views import NoteDetail, NoteList, TagList

urlpatterns = [
    path('notes/', NoteList.as_view()),
    path('note/<int:pk>', NoteDetail.as_view()),
    path('tags/', TagList.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
