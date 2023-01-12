import pytest

from .models import Note


@pytest.mark.fixture
def test_note(db):
    return Note.objects.create(title="note_title", body="note_body")


def test_create_note(db):
    Note.objects.create(title="note_title", body="note_body")

    notes = Note.objects.all()
    assert len(notes) == 1

    note = Note.objects.first()

    assert note.title == "note_title"
    assert note.body == "note_body"


def test_delete_note(db):
    Note.objects.create(title="note_title", body="note_body")

    notes = Note.objects.all()
    assert len(notes) == 1

    note = Note.objects.first()
    note.delete()

    notes = Note.objects.all()
    assert len(notes) == 0


def test_modify_note(db):
    Note.objects.create(title="note_title", body="note_body")

    notes = Note.objects.all()
    assert len(notes) == 1

    note = Note.objects.get()

    assert note.title == "note_title"
    assert note.body == "note_body"

    note.title = "new_title"
    note.body = "new_body"
    note.save()
    note.refresh_from_db()

    assert note.title == "new_title"
    assert note.body == "new_body"
