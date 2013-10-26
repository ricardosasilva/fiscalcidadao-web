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

from django.contrib.gis.db import models
from django.utils.translation import ugettext as _
from multigtfs.models.route import Route
from sorl.thumbnail import ImageField
import os
import uuid

FACT_TYPES = (
    (0, _(u'Suggestion')),
    (1, _(u'Complaint'))
)

class Fact(models.Model):
    description = models.CharField(max_length=30)
    fact_type = models.SmallIntegerField(choices=FACT_TYPES)

    def __unicode__(self):
        return u'%s' % self.description


def occurrence_photo_upload_to(instance, filename):
    _, extension = os.path.splitext(filename)
    return u'occurrence_photos/%s%s' % (uuid.uuid4().hex, extension)


class OccurrenceManager(models.GeoManager):
    pass


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


class Region(models.Model):
    name = models.CharField(max_length=50)
    area = models.PolygonField()
    objects = models.GeoManager()

    def __unicode__(self):
        return u'%s' % self.name
