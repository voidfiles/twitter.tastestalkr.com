#!/usr/bin/env python2.4 
import sys
sys.path += ['/home/varius/django_src']
sys.path += ['/home/varius/django_projects']
from fcgi import WSGIServer
from django.core.handlers.wsgi import WSGIHandler
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'twmusic.settings'
WSGIServer(WSGIHandler()).run()


