#!/usr/bin/env python
import requests, sys, os
from cgi import parse_qs, escape

#for some reason, mod_wsgi doesn't import from the currentd directory. add it to the path
dir = os.path.dirname(__file__)
if dir not in sys.path:
	sys.path.insert(0, dir)

from html_helper import html_escape, build_html_page


#take the metadata about an endpoint and format it for display
def get_metadata ( item ) :

	#put the icon, name, and version into a header tag
	block = '<h2>'
	if item.get('icons'):
		block += '<img src="%s" />' % html_escape(item.get('icons').get('x32'))
		
	#grab the name, default to 'endpoint' if it's not found
	name = html_escape(item.get('name', 'endpoint'))
	
	#if the item has a property called preferred with a value of false, strike out the name
	if not item.get('preferred', True):
		name = '<s>%s</s>' % name
		
	#add the title and version to the heading
	block += '%s - %s</h2>' % (name, html_escape(item.get('version', 'v?')))
	
	#add the description, if there is one
	block += '<p><em>%s</em></p>' % html_escape(item.get('description', 'No Description'))
	
	#check for a "Discovery" URL that contains more info. link to it internally and externally if it exists
	if item.get('discoveryRestUrl') :
		block += '''<a href="?url={0}">Discovery</a>
		<a href="{0}" target="_blank">Discovery (raw)</a>'''.format(html_escape(item.get('discoveryRestUrl')))
	
	#check for a documentation link and link out to it in a new tab/window
	if(item.get('documentationLink')):
		block += '<a href="{0}" target="_blank">Documentation ({0})</a>'.format(html_escape(item.get('documentationLink')))
	return block

# This is the entry point for WSGI python web requests.
def application ( env, start_response ):

	#default URL to call
	api_url = 'https://www.googleapis.com/discovery/v1/apis/'
	
	#env[QUERY_STRING] contains the portion of the URL after the ?, cgi.parse_qs parses it into a dict
	query_params = parse_qs(env['QUERY_STRING'])
	
	#if we were passed a new URL through the request URL, override the default
	if(query_params.get('url')):
		#parse_qs wraps all parameter keys in lists
		api_url = query_params.get('url')[0]
	
	#start building the response body
	response_body = '<div>API Results for <a href="{0}" target="_blank">{0}</a></div>'.format(html_escape(api_url))
	
	#default title, may get overridden
	response_title = "API Discovery Tool"
	
	r = {}
	try :
		#requests.get() makes the HTTP request. .json() parses the result as a json object
		r = requests.get(api_url).json()
	except Exception, e:
		response_body += "<div>Error calling API: %s</div>" % html_escape(str(e))
	
	if r.get('kind'):
		#discovery#directoryList is the listing of all the endpoints 
		if 'discovery#directoryList' == r.get('kind'):
			#iterate the list of APIs and add the formatted metadata to the response
			for item in r['items'] :
				response_body += '<div>%s</div>' % get_metadata(item)
				
		#discovery#restDescription is the details about a single endpoint		
		if 'discovery#restDescription' == r.get('kind'):
		
			#change the title to the name of the web service we're looking at
			if(r.get('name')):
				response_title = r.get('name')
		
			#show the metadata at the top of the response
			response_body += '<div>' + get_metadata(r)
			
			#build a table of all the properties that are just strings
			response_body += '<table><tbody>'
			
			#iterate over every property in the response
			for key in r:
				#if the type of the property is a string, put it in the table
				if isinstance(r.get(key), basestring) :
					response_body += '<tr><td>{0}</td><td>{1}</td></tr>'.format(html_escape(key), html_escape(r.get(key, '-')))
					
			#close the table
			response_body += '</table></div>'
			
			#check the response for a property called "scemas"
			if(r.get('schemas')):
				#iterate over everything in the "schemas" list
				for name in r.get('schemas'):
					schema = r.get('schemas').get(name)
					#show the name in a header with the description below
					response_body += '''<div><h3>Schema: {0}</h3>
					<p>{1}</p>'''.format(html_escape(name), html_escape(schema.get('description', 'no description')))
					
					
					if schema.get('properties'):
						#build a "properties" table
						response_body += '''<h4>Properties:</h4>
						<table>
							<thead>
								<tr><th>Name</th><th>Type</th><th>Description</th>
							</thead>
							<tbody>'''
						#iterate over everything in the schema's "properties" property, and add them to the table
						for propname in schema.get('properties'):
							property = schema.get('properties').get(propname)
							response_body += '<tr><td>{0}</td><td>{1}</td><td>{2}</td></tr>'.format(html_escape(propname), html_escape(property.get('type', '-')), html_escape(property.get('description', '-')))
						response_body += '</tbody></table>'
					response_body += '</div>'
					
	response_html = bytes(build_html_page(response_title, response_body))
	
	# HTTP response code and message
	status = '200 OK'

	response_headers = [
		('Content-Type', 'text/html'),
		('Content-Length', str(len(response_html)))
	]

	# Start the HTTP response by sending the status and headers
	start_response(status, response_headers)

	#send the content
	return [response_html]