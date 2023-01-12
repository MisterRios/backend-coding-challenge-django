import pytest

from .models import Note


@pytest.mark.django_db
def test_create_note():
    Note.objects.create(title="note_title", body="note_body")

    notes = Note.objects.all()
    assert len(notes) == 1

    note = Note.objects.first()

    assert note.title == "note_title"
    assert note.body == "note_body"
