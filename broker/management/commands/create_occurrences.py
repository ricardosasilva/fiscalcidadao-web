import random
from optparse import make_option

from django.contrib.gis.geos import GEOSGeometry, Point
from django.core.management.base import BaseCommand
from model_mommy import mommy
from multigtfs.models import Stop

from broker.models import Occurrence


class Command(BaseCommand):
    help = 'Creates a series of occurrences.'
    option_list = BaseCommand.option_list + (
        make_option('--min',
            dest='min',
            default=0,
            help='Minimum occurrences per stop.'),
        make_option('--max',
            default=20,
            help='Maximum occurrences per stop.'),
        )

    def handle(self, *args, **options):
        stops = Stop.objects.all().values('lat', 'lon')
        minimum = options['min']
        maximum = options['max']
        for stop in stops:
            latitude = stop['lat']
            longitude = stop['lon']
            #location = Point(longitude, latitude)
            location = GEOSGeometry('POINT({} {})'.format(longitude, latitude))
            quantity = random.randint(minimum, maximum)
            users = mommy.make(Occurrence, quantity, location=location)
