# -*- coding: utf-8 -*-
#
# Copyright (c) 2013,
# Diogo Baeder, Francisco Ciliao, Gabriel Palacio, Ricardo Silva, Vitor George
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modificat-
# ion, are permitted provided that the following conditions are met:
#
#  - Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#  - Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#

from broker.models import Occurrence, Fact
from django.contrib.gis.geos.point import Point
from django.core.management.base import BaseCommand
from multigtfs.models.route import Route
from multigtfs.models.stop import Stop
from optparse import make_option
from random import choice
from utils import randomDate
import random


def random_stop_position():
    stop = Stop.objects.filter().order_by('?')[0]
    point = Point(float(stop.lon), float(stop.lat), srid=4326)
    return point

def random_photo():
    photos = (
        'occurrence_photos/1.jpg',
        None,
        'occurrence_photos/2.jpg',
        'occurrence_photos/3.jpg',
        None,
        None)
    return choice(photos)

def random_comment():
    comments = (
        u'Precisa melhorar',
        '',
        '',
        u'Não gostei',
        '',
        '',
        '',
    )
    return choice(comments)

def get_date():
    return randomDate("2010-9-1 00:00+0300", "2013-10-26 23:50+0300", random.random())

def get_bus_fact():
    fact = Fact.objects.filter(pk__in=(1,2,3,4,5,6,7,8)).order_by('?')[0]
    return fact

def get_route():
    routes = Route.objects.all().order_by('?')[0]
    return routes


class Command(BaseCommand):
    help = 'Creates a series of bus occurrences.'
    option_list = BaseCommand.option_list + (
        make_option('--quantity',
            default=10,
            dest = 'qtd',
            help='Quantity of occurrences'),
        )

    def handle(self, *args, **options):
        quantity = int(options['qtd'])
        for i in range(1, quantity):
            occurrence = Occurrence() 
            occurrence.date_time = get_date()
            occurrence.fact = get_bus_fact()
            occurrence.location = random_stop_position()
            occurrence.route = get_route()
            occurrence.comment = random_comment()
            occurrence.photo = random_photo()
            occurrence.save()