import pytest

from django.urls import reverse


@pytest.mark.django_db
def test_create(auth_user, category):
    payload = {
        "category": category.pk,
        "title": "Title new goal",
        "description": "New Description",
        "due_date": "2024-12-26",
        "status": 1,
        "priority": 1
    }

    response = auth_user.post(reverse('goal_create'), data=payload)

    answer = {
        "id": response.data.get('id'),
        "category": category.pk,
        "created": response.data.get('created'),
        "updated": response.data.get('updated'),
        "title": "Title new goal",
        "description": "New Description",
        "due_date": "2024-12-26",
        "status": 1,
        "priority": 1
    }

    assert response.data == answer
    assert response.status_code == 201


@pytest.mark.django_db
def test_list(auth_user, goal):
    response = auth_user.get(reverse('goal_list'))

    assert response.status_code == 200


@pytest.mark.django_db
def test_get(auth_user, goal):
    response = auth_user.get(reverse('goal_update', args=[goal.pk]))

    assert response.status_code == 200


@pytest.mark.django_db
def test_update(auth_user, goal, category):
    payload = {
        "title": "Test update title",
        "category": category.pk
    }
    response = auth_user.put(reverse('goal_update', args=[goal.pk]), payload)

    assert response.status_code == 200
    assert response.data.get('title') == 'Test update title'


@pytest.mark.django_db
def test_delete(auth_user, goal):
    response = auth_user.delete(reverse('goal_update', args=[goal.pk]))

    assert response.status_code == 204
