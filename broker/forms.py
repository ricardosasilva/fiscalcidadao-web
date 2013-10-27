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
from django import forms
from django.contrib.gis.geos.point import Point
from django.core.exceptions import ValidationError
from multigtfs.models.route import Route
import logging
import time

logger = logging.getLogger(__name__)

class OccurrenceForm(forms.Form):
    fact = forms.IntegerField()
    date_time = forms.CharField(max_length=64)
    latitude = forms.FloatField()
    longitude = forms.FloatField()
    route = forms.CharField(required=False)
    comment = forms.CharField(required=False)
    photo = forms.ImageField(required=False)
    phone = forms.CharField(max_length=20, required=False)

    def clean_fact(self):
        fact_id = self.cleaned_data['fact']
        try:
            self.fact = Fact.objects.get(pk=fact_id)
        except Fact.DoesNotExist():
            raise ValidationError(u'Fact not found')
        return fact_id

    def clean_date_time(self):
        try:
            date_time = int(self.cleaned_data['date_time'])
            new_date_time = time.strftime('%Y-%m-%d %H:%M:%S',  time.gmtime(date_time/1000))
            return new_date_time
        except Exception, exc:
            logger.exception(exc)
            raise ValidationError(u'Error in date_time format')

    def clean_route(self):
        route_id = self.cleaned_data['route']
        try:
            self.route = Route.objects.get(route_id=route_id)
        except Route.DoesNotExist:
            raise ValidationError(u'Route not found')

    def save(self, ip_address):
        latitude = self.cleaned_data['latitude']
        longitude = self.cleaned_data['longitude']
        
        occurrence = Occurrence()
        occurrence.fact = self.fact
        occurrence.date_time = self.cleaned_data['date_time']
        occurrence.location = Point(y=latitude, x=longitude, srid=4326)
        occurrence.route = self.route
        occurrence.ip_address = ip_address
        if self.photo:
            occurrence.photo = self.photo
        return occurrence.save()