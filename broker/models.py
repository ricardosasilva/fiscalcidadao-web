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

from datetime import datetime, timedelta
from django.contrib.gis.db import models
from django.db.models import Count
from django.utils.translation import ugettext as _
from multigtfs.models.route import Route
from sorl.thumbnail import ImageField
import os
import uuid



SUGGESTION_FACT = 0
COMPLAINT_FACT = 1


FACT_TYPES = (
    (SUGGESTION_FACT, _(u'Suggestion')),
    (COMPLAINT_FACT, _(u'Complaint'))
)


class FactManager(models.Manager):

    def complaints(self):
        past = datetime.now() - timedelta(days=30)
        facts = self.filter(fact_type=COMPLAINT_FACT, occurrence__date_time__gte=past)
        return facts.annotate(num_occurrencies=Count('occurrence')).values('description', 'num_occurrencies')

    def complaints_over_time(self):
        result = {}
        minus_1 = datetime.now() - timedelta(days=30)
        minus_2 = datetime.now() - timedelta(days=60)
        minus_3 = datetime.now() - timedelta(days=90)
        minus_4 = datetime.now() - timedelta(days=120)

        result[30] = Fact.objects.filter(occurrence__date_time__gt=minus_1).annotate(total_occurrences=Count('occurrence')).values('id', 'description', 'total_occurrences')
        result[60] = Fact.objects.filter(occurrence__date_time__gt=minus_2, occurrence__date_time__lt=minus_1).annotate(total_occurrences=Count('occurrence')).values('id', 'description', 'total_occurrences')
        result[90] = Fact.objects.filter(occurrence__date_time__gt=minus_3, occurrence__date_time__lt=minus_2).annotate(total_occurrences=Count('occurrence')).values('id', 'description', 'total_occurrences')
        result[120] = Fact.objects.filter(occurrence__date_time__gt=minus_4, occurrence__date_time__lt=minus_3).annotate(total_occurrences=Count('occurrence')).values('id', 'description', 'total_occurrences')
        
        series = []
        for fact in super(FactManager, self).filter(pk__lte=8):
            serie = {}
            serie['name'] = fact.description
            serie['data'] = []
            try:
                serie['data'].append(result[30].get(id=fact.id)['total_occurrences'])
            except:
                serie['data'].append(0)

            try:
                serie['data'].append(result[60].get(id=fact.id)['total_occurrences'])
            except:
                serie['data'].append(0)
            try:
                serie['data'].append(result[90].get(id=fact.id)['total_occurrences'])
            except:
                serie['data'].append(0)
            try:
                serie['data'].append(result[120].get(id=fact.id)['total_occurrences'])
            except:
                serie['data'].append(0)

            series.append(serie)
        return series

class Fact(models.Model):
    description = models.CharField(max_length=30)
    fact_type = models.SmallIntegerField(choices=FACT_TYPES)

    objects = FactManager()

    def __unicode__(self):
        return u'%s' % self.description


def occurrence_photo_upload_to(instance, filename):
    _, extension = os.path.splitext(filename)
    return u'occurrence_photos/%s%s' % (uuid.uuid4().hex, extension)


class OccurrenceManager(models.GeoManager):
    def points(self):
        past = datetime.now() - timedelta(days=30)
        occurrences = self.filter(date_time__gte=past)
        for point in occurrences.values('location'):
            yield point


class Occurrence(models.Model):
    fact = models.ForeignKey(Fact)
    date_time = models.DateTimeField()
    location = models.PointField(srid=4326, null=True, blank=True)
    route = models.ForeignKey(Route, null=True, blank=True)
    comment = models.TextField(blank=True)
    photo = ImageField(blank=True, upload_to=occurrence_photo_upload_to)
    ip_address = models.CharField(max_length=15, blank=True)
    phone = models.CharField(max_length=20, blank=True, db_index=True)

    objects = OccurrenceManager()

    def __unicode__(self):
        return u'%s' % self.pk


class RegionManager(models.GeoManager):

    def total_occurrences(self):
        result = {}
        for region in Region.objects.all():
            past = datetime.now() - timedelta(days=30)
            total_occurrences = Occurrence.objects.filter(location__within=region.area, date_time__gte=past).count()
#            occurrences = Occurrence.objects.filter(location__within=region.area).order_by('fact').annotate(Count('fact'))
#            facts = Fact.objects.filter(occurrence__in=occurrences).annotate(total_occurrences=Count('occurrence')).values('id', 'total_occurrences')
            result[region.id] = total_occurrences
        return result


class Region(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=10, blank=True)
    area = models.MultiPolygonField()

    objects = RegionManager()

    def __unicode__(self):
        return u'%s' % self.name
