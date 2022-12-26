import factory.fuzzy

from core.models import User
from goals.models import Board, GoalCategory, Goals, GoalComment, BoardParticipant


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker('TestUser')
    email = factory.Faker('test@mail.ru')
    password = 'PasswordsTest123'


class BoardFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Board

    title = factory.fuzzy.FuzzyText(length=25)


class BoardParticipantFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BoardParticipant

    board = factory.SubFactory(BoardFactory)
    user = factory.SubFactory(UserFactory)


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = GoalCategory

    board = factory.SubFactory(BoardFactory)
    title = factory.fuzzy.FuzzyText(length=10)
    user = factory.SubFactory(UserFactory)


class GoalFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Goals

    title = factory.fuzzy.FuzzyText(length=10)
    user = factory.SubFactory(UserFactory)
    category = factory.SubFactory(CategoryFactory)


class CommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = GoalComment

    text = factory.fuzzy.FuzzyText(length=10)
    goal = factory.SubFactory(UserFactory)
    user = factory.SubFactory(GoalFactory)


