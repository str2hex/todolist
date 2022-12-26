import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_create(client) -> None:
    payload = {
        "username": "string",
        "first_name": "string",
        "last_name": "string",
        "email": "user@example.com",
        "password": "stringstring",
        "password_repeat": "stringstring"
    }

    response = client.post(reverse('signup'), data=payload)

    answer = {
        "id": response.data.get('id'),
        "username": "string",
        "first_name": "string",
        "last_name": "string",
        "email": "user@example.com",
    }

    assert response.data == answer
    assert response.status_code == 201


@pytest.mark.django_db
def test_login(client, add_user) -> None:
    payload = {
        'username': 'TestUser',
        'password': 'PasswordsTest123'
    }

    response = client.post(reverse('login'), data=payload)

    assert response.status_code == 200


@pytest.mark.django_db
def test_login_fail(client, add_user):
    payload = {
        'username': 'FailUser',
        'password': 'FailPasswords'
    }

    response = client.post(reverse('login'), data=payload)

    assert response.status_code == 403


@pytest.mark.django_db
def test_user_update(auth_user):
    payload = {
        "username": "updateUsername",
        "first_name": "updateFirstname",
        "last_name": "updateLastname",
        "email": "updateUser@mail.ru"
    }

    response = auth_user.put(reverse('profile'), payload)

    answer = {
        "id": response.data.get('id'),
        "username": "updateUsername",
        "first_name": "updateFirstname",
        "last_name": "updateLastname",
        "email": "updateUser@mail.ru"
    }

    assert response.data == answer
    assert response.status_code == 200


@pytest.mark.django_db
def test_get(auth_user):
    response = auth_user.get(reverse('profile'))

    data = response.data

    answer = {
        "id": data.get('id'),
        "username": "TestUser",
        "first_name": "",
        "last_name": "",
        "email": "test@mail.ru"
    }

    assert response.status_code == 200
    assert data == answer


@pytest.mark.django_db
def test_change_password(auth_user):
    payload = {
        "old_password": "PasswordsTest123",
        "new_password": "NewPasswordsTest123"
    }

    response = auth_user.put(reverse('update_password'), payload)

    assert response.status_code == 200


@pytest.mark.django_db
def test_user_change_password_fail(auth_user):
    payload = {
        "old_password": "PasswordsTest1234",
        "new_password": "NewPasswordsTest123"
    }

    response = auth_user.put(reverse('update_password'), payload)

    assert response.status_code == 400


@pytest.mark.django_db
def test_change_password_validate_new_password(auth_user):
    payload = {
        "old_password": "PasswordsTest123",
        "new_password": "1234"
    }

    response = auth_user.put(reverse('update_password'), payload)

    assert response.status_code == 400
