import pytest

from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from core.models import User
from goals.models import Board, BoardParticipant, GoalCategory, Goals, GoalComment
from tests.factories import BoardFactory, BoardParticipantFactory, CategoryFactory, GoalFactory, CommentFactory

USER_MODEL = get_user_model()

@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def add_user() -> USER_MODEL:
    user = User.objects.create_user(username='TestUser',
                                    email='test@mail.ru',
                                    password='PasswordsTest123')
    return user


@pytest.fixture
def auth_user(add_user, client) -> APIClient:
    client.login(username='TestUser', password='PasswordsTest123')
    return client


@pytest.fixture
def board(auth_user) -> Board:
    return BoardFactory.create()


@pytest.fixture
def board_participant(add_user, board) -> BoardParticipant:
    return BoardParticipantFactory.create(user=add_user, board=board)


@pytest.fixture
def category(board, add_user, board_participant) -> GoalCategory:
    return CategoryFactory.create(board=board, user=add_user)


@pytest.fixture
def goal(category, add_user) -> Goals:
    return GoalFactory.create(user=add_user, category=category)


@pytest.fixture
def comment(goal, add_user) -> GoalComment:
    return CommentFactory.create(user=add_user, goal=goal)
