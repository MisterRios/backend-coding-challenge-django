import pytest

from .models import Note, Tag


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


def test_create_tag(db):
    Tag.objects.create(name="test_name")

    tags = Tag.objects.all()
    assert len(tags) == 1

    tag = Tag.objects.first()

    assert tag.name == "test_name"


def test_delete_tag(db):
    Tag.objects.create(name="test_name")

    tags = Tag.objects.all()
    assert len(tags) == 1

    tag = Tag.objects.get()
    tag.delete()

    notes = Tag.objects.all()
    assert len(notes) == 0


def test_modify_tag(db):
    Tag.objects.create(name="test_name")

    tag = Tag.objects.get()

    tag.name = "new_name"
    tag.save()
    tag.refresh_from_db()

    assert tag.name == "new_name"


def test_add_tag_to_note(db):
    Note.objects.create(title="note_title", body="note_body")
    Tag.objects.create(name="test_name")

    note = Note.objects.get()
    tag = Tag.objects.get()

    note.tags.add(tag)
    note.save()

    assert len(note.tags.all()) == 1

    note.refresh_from_db()

    assert note.tags.get() == tag


def test_delete_tag_from_note(db):
    Note.objects.create(title="note_title", body="note_body")
    Tag.objects.create(name="test_name")

    note = Note.objects.get()
    tag = Tag.objects.get()

    note.tags.add(tag)
    note.save()

    note.tags.remove(tag)
    note.save()
    note.refresh_from_db()

    assert len(note.tags.all()) == 0
