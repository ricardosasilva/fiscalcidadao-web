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

from broker.models import Fact, Occurrence, Region
from django.contrib.gis import admin
from multigtfs.models.route import Route
from multigtfs.models.stop import Stop
from multigtfs.models.trip import Trip


class FactAdmin(admin.ModelAdmin):
    list_fields = ('description', 'fact_type')


class OccurrenceAdmin(admin.OSMGeoAdmin):
    list_fields = ('description', 'fact_type')
    list_filter = ('date_time',)


admin.site.register(Fact, FactAdmin)
admin.site.register(Occurrence, OccurrenceAdmin)
admin.site.register(Region, admin.OSMGeoAdmin)


class StopAdmin(admin.ModelAdmin):
    raw_id_fields = ('parent_station',)

class RouteAdmin(admin.ModelAdmin):
    list_filter = ('rtype',)

class TripAdmin(admin.ModelAdmin):
    raw_id_fields = ('route', 'services', 'shape')

admin.site.unregister(Stop)
admin.site.unregister(Route)
admin.site.unregister(Trip)

admin.site.register(Stop, StopAdmin)
admin.site.register(Route, RouteAdmin)
admin.site.register(Trip, TripAdmin)