import pytest

from django.urls import reverse


@pytest.mark.django_db
def test_create(auth_user, goal):
    payload = {"text": "New title comments",
               "goal": goal.pk
               }

    response = auth_user.post(reverse('goal_comment_create'), data=payload)

    answer = {
        "id": response.data.get('id'),
        "created": response.data.get('created'),
        "updated": response.data.get('updated'),
        "text": "New title comments",
        "goal": str(goal.pk)
    }

    assert response.data == answer


@pytest.mark.django_db
def test_list(auth_user, comment):
    response = auth_user.get(reverse('goal_comment_list'))

    assert response.status_code == 200


@pytest.mark.django_db
def test_get(auth_user, comment):
    response = auth_user.get(reverse('goal_comment_update', args=[comment.pk]))

    assert response.status_code == 200


@pytest.mark.django_db
def test_update(auth_user, goal, comment):
    payload = {
        "text": "Text update string",
        "goal": goal.pk
    }

    response = auth_user.put(reverse('goal_comment_update', args=[comment.pk]), data=payload)

    assert response.status_code == 200
    assert response.data.get('text') == 'Text update string'


@pytest.mark.django_db
def test_delete(auth_user, goal, comment):
    response = auth_user.delete(reverse('goal_comment_update', args=[comment.pk]))

    assert response.status_code == 204
