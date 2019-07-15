"""Factories for creating fake data."""

from django.contrib.auth import get_user_model

import factory
from faker import Factory

from groups.models import Group

faker = Factory.create()


class GroupFactory(factory.DjangoModelFactory):
    """Factory for posts creating."""

    class Meta:
        model = Group

    name = factory.LazyAttribute(lambda o: faker.sentence(nb_words=4))
    description = factory.LazyAttribute(lambda o: faker.text())


class UserFactory(factory.DjangoModelFactory):
    """Factory for users creating."""

    class Meta:
        model = get_user_model()
        django_get_or_create = ('username',)

    username = factory.LazyAttribute(lambda o: faker.name())
    email = factory.LazyAttribute(lambda o: faker.email())
    password = factory.PostGenerationMethodCall(
        'set_password', 'default_password'
    )
    group = factory.SubFactory(GroupFactory)
