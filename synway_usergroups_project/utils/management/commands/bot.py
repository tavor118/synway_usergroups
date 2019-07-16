"""
Custom management command for creating users and groups.
Run:
`python manage.py bot`
"""

import json
import os
import random
from django.core.management.base import BaseCommand

from config.settings import BASE_DIR
from seed.factories import (UserFactory,
                            GroupFactory)


def get_configuration():
    """
    Get configuration for bot from `bot_config.json` file.
    :return: Dictionary with configurations.
    """
    config_file = os.path.join(BASE_DIR, 'bot_config.json')
    with open(config_file) as config:
        return json.load(config)


def create_groups(max_groups):
    """
    Create groups.
    :param max_groups: Maximum count of groups.
    :return: Created groups.
    """
    groups = GroupFactory.create_batch(max_groups)
    return groups


def create_users(number_of_users, groups):
    """
    Create given number of users.
    :param number_of_users:
    :param groups: Groups for user participation.
    :return: Created users.
    """
    all_users = []
    for group in groups:
        users = UserFactory.create_batch(
            random.randint(0, number_of_users), group=group
        )
        all_users += users
    return all_users


class Command(BaseCommand):
    """
    Custom management command for creating users, posts and likes for them.
    """

    help = 'Bot for creating users, posts and likes for them.'

    def handle(self, *args, **kwargs): #pylint: disable=unused-argument

        config = get_configuration()

        groups = create_groups(config['max_groups'])
        self.stdout.write(self.style.SUCCESS(
            f'Successfully created such groups: {groups}.'
        ))

        users = create_users(config['number_of_users'], groups)
        self.stdout.write(self.style.SUCCESS(
            f'Successfully created such users: {users}.'
        ))


