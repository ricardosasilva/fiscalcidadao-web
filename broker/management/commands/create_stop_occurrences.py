# -*- coding: utf-8 -*-
from broker.management.commands.create_bus_occurrences import get_date, \
    random_stop_position, get_route, random_comment, random_photo
from broker.models import Fact, Occurrence
from django.core.management.base import BaseCommand
from optparse import make_option

def get_stop_fact():
    fact = Fact.objects.filter(pk__in=(9,10,11,12,13)).order_by('?')[0]
    return fact


class Command(BaseCommand):
    help = 'Creates a series of stop occurrences.'
    option_list = BaseCommand.option_list + (
        make_option('--quantity',
            default=10,
            dest = 'qtd',
            help='Quantity of occurrences'),
        )

    def handle(self, *args, **options):
        quantity = options['qtd']
        for i in range(1, quantity):
            occurrence = Occurrence() 
            occurrence.date_time = get_date()
            occurrence.fact = get_stop_fact()
            occurrence.location = random_stop_position()
            occurrence.route = get_route()
            occurrence.comment = random_comment()
            occurrence.photo = random_photo()
            occurrence.save()