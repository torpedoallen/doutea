import os
import sys
import traceback
from django.core.handlers.wsgi import WSGIHandler
from django.core.signals import got_request_exception
from django.core.management import call_command
#from dae.api.onimaru.onimaru import send as onimaru_send

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'doutea'))
os.environ['DJANGO_SETTINGS_MODULE'] = 'doutea.settings'

def exception_printer(sender, **kwargs):
    #onimaru_send({'data': kwargs,'request': {}, 'site': 'doutea.dapps.douban.com'})
    traceback.print_exc()

got_request_exception.connect(exception_printer)
#call_command('syncdb')
app = WSGIHandler()
