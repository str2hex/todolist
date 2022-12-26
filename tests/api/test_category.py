from django.urls import reverse

import pytest


@pytest.mark.django_db
def test_create(board, auth_user, add_user, board_participant):
    payload = {
        "user": add_user.pk,
        "title": "Test string",
        "board": board.pk
    }

    response = auth_user.post(reverse('category_create'), payload)

    answer = {
        "id": response.data.get('id'),
        "created": response.data.get('created'),
        "updated": response.data.get('updated'),
        "title": "Test string",
        "is_deleted": False,
        "board": response.data.get('board')
    }

    assert response.data == answer
    assert response.status_code == 201


@pytest.mark.django_db
def test_list(board, auth_user, board_participant, category):
    response = auth_user.get(reverse('goal_category_list'))

    assert response.status_code == 200


@pytest.mark.django_db
def test_get(board, board_participant, category, auth_user):
    response = auth_user.get(reverse('goal_category_update', args=[category.pk]))
    assert response.status_code == 200


@pytest.mark.django_db
def test_update(board, category, auth_user, board_participant, add_user):
    payload = {
        "title": "Test update title",
        "is_deleted": True,
        "board": board.pk
    }

    response = auth_user.put(reverse('goal_category_update', args=[category.pk]), data=payload)

    answer = {
        "id": category.pk,
        "user": {
            "id": add_user.pk,
            "username": "TestUser",
            "first_name": "",
            "last_name": "",
            "email": "test@mail.ru"
        },
        "created": response.data.get('created'),
        "updated": response.data.get('updated'),
        "title": "Test update title",
        "is_deleted": True,
        "board": board.pk
    }

    assert response.data == answer


@pytest.mark.django_db
def test_delete(board, board_participant, category, auth_user):
    response = auth_user.delete(reverse('goal_category_update', args=[category.pk]))

    assert response.status_code == 204
