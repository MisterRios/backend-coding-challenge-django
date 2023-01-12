from django.urls import reverse
from notes.models import Note, Tag
from rest_framework.test import APIClient

NOTES_URL = reverse("notes")
TAGS_URL = reverse("tags")


def get_note_url(id):
    return reverse("note", kwargs={"pk": id})


AUTH_KWARGS = {"username": "someone", "password": "something"}


def test_api_list_notes(db, django_user_model):
    owner = django_user_model.objects.create(**AUTH_KWARGS)
    # TODO: use fixtures to create test client instead of
    # instantiating over and over

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

    test_client = APIClient()
    expected = [
        {
            'id': 1,
            'title': 'note_title',
            'body': 'note_body',
            'tags': [{'id': 1, 'name': 'name'}],
            'owner': 'someone',
        },
        {
            'id': 2,
            'title': 'note_title2',
            'body': 'note_body2',
            'tags': [{'id': 2, 'name': 'name2'}],
            'owner': 'someone',
        },
    ]

    # test without authentication
    response = test_client.get(NOTES_URL)

    assert response.json() == expected

    # test with authentication
    test_client.force_authenticate(user=owner)
    response = test_client.get(NOTES_URL)

    assert response.json() == expected


def test_create_notes(db, django_user_model):
    owner = django_user_model.objects.create(**AUTH_KWARGS)
    # TODO: test with tags included in create notes payload
    test_client = APIClient()
    test_client.force_authenticate(user=owner)

    payload = {'title': 'note_title', 'body': 'note_body', 'tags': [], "owner": owner.id}

    test_client.post(NOTES_URL, payload)

    response = test_client.get(NOTES_URL)

    assert response.json() == [
        {
            'id': 1,
            'title': 'note_title',
            'body': 'note_body',
            'tags': [],
            'owner': 'someone',
        }
    ]


def test_delete_notes(db, django_user_model):
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

    response = test_client.get(NOTES_URL)

    first_note_id = response.json()[0]['id']

    url = get_note_url(id=first_note_id)

    response = test_client.delete(url)

    assert response.status_code == 204

    response = test_client.get(NOTES_URL)

    assert len(response.json()) == 1
    assert response.json()[0]['id'] == 2


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
