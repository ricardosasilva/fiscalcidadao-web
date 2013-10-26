from optparse import make_option

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from mockups import Mockup


class Command(BaseCommand):
    help = 'Creates a series of users.'
    option_list = BaseCommand.option_list + (
        make_option('-n', '--number-of-users',
            dest='number_of_users',
            default=10,
            help='The number of users to create.'),
        )

    def handle(self, *args, **options):
        number_of_users = int(options['number_of_users'])
        mockup = Mockup(User)
        users = mockup.create(number_of_users)
