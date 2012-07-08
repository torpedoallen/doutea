# -*- coding: utf-8 -*-

from django.http import HttpResponse
import django.utils.simplejson as json

class JSONResponse(HttpResponse):
    def __init__(self, object, status=200):
        content = json.dumps(object)
        return HttpResponse.__init__(self, content=content, status=status, content_type="application/json")
