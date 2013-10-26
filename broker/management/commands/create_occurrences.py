from optparse import make_option

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from model_mommy import mommy

from broker.models import Occurrence


class Command(BaseCommand):
    help = 'Creates a series of occurrences.'
    option_list = BaseCommand.option_list + (
        make_option('-q', '--quantity',
            dest='quantity',
            default=10,
            help='Quantity of items to generate.'),
        make_option('-f', '--file',
            dest='file',
            help='File to read the data from.'),
        )

    def handle(self, *args, **options):
        quantity = int(options['quantity'])
        with open(options['file']) as f:
            for point in points:
                latitude = point[3]
                longitude = point[4]
                users = mommy.make(Occurrence, quantity, latitude=latitude, longitude=longitude)
