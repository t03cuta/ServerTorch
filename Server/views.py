# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from requests import *


@csrf_exempt
def index(request):
    if request.method == "POST":
        response = postRequest(request)
        return JsonResponse(response, safe=False)

    elif request.method == "GET":
        response = getRequest(request)
        return HttpResponse("Response: %s" % str(response))

    else:
        return HttpResponse("Anything else response")
