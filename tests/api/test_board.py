import json

import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_create(board, auth_user) -> None:
    response = auth_user.post(reverse('board_create'), data={'title': 'test board', }, )

    answer = {
        'id': response.data.get('id'),
        'title': 'test board',
        'created': response.data.get('created'),
        'updated': response.data.get('updated'),
        'is_deleted': False,
    }

    assert response.status_code == 201
    assert response.data == answer


@pytest.mark.django_db
def test_list(board, board_participant, auth_user):
    response = auth_user.get(reverse('board_list'))

    assert response.status_code == 200


@pytest.mark.django_db
def test_get(board, board_participant, auth_user):
    response = auth_user.get(reverse('board_update', args=[board.pk]))

    assert response.status_code == 200


@pytest.mark.django_db
def test_update(board, board_participant, auth_user, add_user):
    payload = {
        'title': 'Test update board title',
        'participants': [],
    }

    response = auth_user.put(reverse('board_update', args=[board.pk]), data=json.dumps(payload),
                             content_type='application/json')

    assert response.status_code == 200
    assert response.data.get('title') == 'Test update board title'


@pytest.mark.django_db
def test_delete(board, board_participant, auth_user):
    response = auth_user.delete(reverse('board_update', args=[board.pk]))

    assert response.status_code == 204
