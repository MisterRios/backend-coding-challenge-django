from django.urls import reverse
from notes.models import Note, Tag
from rest_framework.test import APIClient

NOTES_URL = reverse("notes")
AUTH_KWARGS = {"username": "someone", "password": "something"}


def test_api_filter_by_tag(db, django_user_model):
    owner = django_user_model.objects.create(**AUTH_KWARGS)

    test_client = APIClient()
    test_client.force_authenticate(user=owner)

    # TODO: use factory_boy to create multiple test objects for easier testing
    Tag.objects.create(name="name")
    tag1 = Tag.objects.get(id=1)
    Tag.objects.create(name="name2")
    tag2 = Tag.objects.get(id=2)

    Note.objects.create(title="note_title", body="note_body", owner=owner)
    note_1 = Note.objects.get(id=1)
    note_1.tags.add(tag1)
    note_1.save()
    Note.objects.create(title="note_title2", body="note_body2", owner=owner)
    note_2 = Note.objects.get(id=2)
    note_2.tags.add(tag2)
    note_2.save()

    expected = [
        {
            'id': 2,
            'title': 'note_title2',
            'body': 'note_body2',
            'tags': [{'id': 2, 'name': 'name2'}],
            'owner': 'someone',
        }
    ]
    url = f"{NOTES_URL}?tag=name2"

    response = test_client.get(url)

    assert response.json() == expected


def test_api_list_notes(db, django_user_model):
    owner = django_user_model.objects.create(**AUTH_KWARGS)
    test_client = APIClient()
    test_client.force_authenticate(user=owner)

    Tag.objects.create(name="name1")
    tag1 = Tag.objects.get(id=1)
    Tag.objects.create(name="name2")
    tag2 = Tag.objects.get(id=2)

    Note.objects.create(title="Apples Oranges", body="I like to eat fruit", owner=owner)
    note_1 = Note.objects.get(id=1)
    note_1.tags.add(tag1)
    note_1.save()
    Note.objects.create(
        title="Chocolate Cake", body="Flour eggs milk sugar chocolate", owner=owner
    )
    note_2 = Note.objects.get(id=2)
    note_2.tags.add(tag2)
    note_2.save()

    expected_fruit = [
        {
            'id': 1,
            'title': 'Apples Oranges',
            'body': 'I like to eat fruit',
            'tags': [{'id': 1, 'name': 'name1'}],
            'owner': 'someone',
        }
    ]

    expected_cake = [
        {
            'id': 2,
            'title': 'Chocolate Cake',
            'body': 'Flour eggs milk sugar chocolate',
            'tags': [{'id': 2, 'name': 'name2'}],
            'owner': 'someone',
        }
    ]

    url = f"{NOTES_URL}?search=fruit"

    response = test_client.get(url)

    assert response.json() == expected_fruit

    url = f"{NOTES_URL}?search=cake"
    response = test_client.get(url)

    assert response.json() == expected_cake
