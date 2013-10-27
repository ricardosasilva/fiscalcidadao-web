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
from broker.forms import OccurrenceForm
from broker.models import Fact, Occurrence, Region
from django.http.response import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
import uuid


def report_total_per_region(request):
    result = Region.objects.total_occurrences()
    return HttpResponse(json.dumps(result))


def report_occurrences_points(request):
    result = [{
        'lat': point['location'].y,
        'lon': point['location'].x,
        'value': 0.1,
    } for point in Occurrence.objects.points()]
    return HttpResponse(json.dumps(result))


def report_facts_complaints(request):
    result = [[complaint['description'], complaint['num_occurrencies']]
              for complaint in Fact.objects.complaints()]
    return HttpResponse(json.dumps(result))

def report_facts_evolution(request):
    result = Fact.objects.complaints_over_time()
    return HttpResponse(json.dumps(result))

def handle_uploaded_file(f):
    with open(u'occurrence_photos/%s.jpg' % uuid.uuid4().hex, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

@require_POST
@csrf_exempt
def post_ocurrence(request):
    print request
    form = OccurrenceForm(request.POST, request.FILES)
    if form.is_valid():
        handle_uploaded_file(request.FILES['photo'])
        occurrence = form.save(ip_address=request.META['REMOTE_ADDR'])
        return HttpResponse('ok')
    else:
        return HttpResponseBadRequest('Bad request: please check your data')