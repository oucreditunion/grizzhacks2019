#!/usr/bin/env python
from cgi import escape

#escape reserved HTML characters, and convert non-ascii characters into entity references
def html_escape( raw ) :
	return (escape(raw).encode('ascii', 'xmlcharrefreplace'))
	
def build_html_page(title, body):
	#basic boilerplate template for html output, with a little css sprinkled in
	page = '''<!doctype HTML>
<html>
    <head>
		<style type="text/css">
			body {{ background-color:#eeeeee; font-family:sans-serif; }}
			table {{ border-collapse: collapse; }}
			td,a {{ padding: 5px; }}
			td {{border:solid 1px #999999;}}
			a{{display:block;}}
			div {{
				border: solid 1px #dddddd;
				padding: 1em;
				margin: 1em;
				background-color:#FFFFFF;
				box-shadow:#cccccc 5px 5px 2px;
			}}
		</style>
		<title>{0}</title>
    </head>
    <body>
		{1}
	</body>
</html>'''.format(escape(title), body)
	return page
