#!/usr/bin/python

import api_discovery
from wsgiref.simple_server import make_server
httpd = make_server('', 8081, api_discovery.application)
httpd.serve_forever()