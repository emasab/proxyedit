def init(proxy):

	# Replace a page with a local file
	if proxy.match("^https\:\/\/www.google.it\/$"):
		proxy.response.body.replace.file("./content.html")

	# Disable client and bypass proxy cache
	#if proxy.match("^https\:\/\/www.google.it\/$"):
	#	proxy.nocache()
	#	proxy.noproxycache(randomize_param="kwnocache")
	

	# Add or replace an header
	#if proxy.match("^https\:\/\/www.google.it\/$"):
	#	proxy.response.header.add("set-cookie", "proxy=1; max-age=31536000; expires=Tue, 07 Jun 2016 15:32:22 GMT;path=/; domain=.google.it;")
	#	proxy.response.header.replace("set-cookie", "proxy=1; max-age=31536000; expires=Tue, 07 Jun 2016 15:32:22 GMT;path=/; domain=.google.it;")
	#	proxy.request.header.add("Cookie", "proxy=1;")
	#	proxy.request.header.replace("Cookie", "proxy=2;")

	# Replace the content with an url
	#if proxy.match("^https\:\/\/www.google.it\/$"):
	#	proxy.response.body.replace.url("http://www.bing.com/")


	# Replace in the original content using a regex
	#if proxy.match("^https\:\/\/www.google.it\/$"):
	#	proxy.response.body.replace.regex("www\.google", "www.yahoo")	

	# Add or replace query parameters
	#if proxy.match("^https\:\/\/www.google.it\/$"):
	#	proxy.response.query.add("proxy", "1")
	#	proxy.response.query.replace("proxy", "2")

	# Replace the host, port and path
	#if proxy.match("^https\:\/\/www.google.it\/$"):
	#	proxy.request.host.replace("localhost")
	#	proxy.request.port.replace(81)
	#	proxy.request.path.replace("/google.html")

	# Save the captured flow in a .har file
	#proxy.savehar("./log.har")

	
