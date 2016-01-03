# ProxyEdit

ProxyEdit is a configurable filter for mitmproxy. Using the configuration file most of the parts ot the http protocol can be changed: the headers, the body, the query string and so on.

## Prerequisites

Mitmproxy must be installed

http://docs.mitmproxy.org/en/latest/install.html


## Run

It can be run with sh

```sh
sh proxyedit.sh
```

or directly with mitmdump

```sh
mitmdump -p 8081 -s scripts/filter.py
```

## Configuration

The configurations is placed in conf.py, it's a DSL that uses python.
What can be done:

#### Replace a page with a local file
```python
if proxy.match("^https\:\/\/www.google.it\/$"):
  proxy.response.body.replace.file("./content.html")
```
#### Replace the request body, filter expression work too
```python
if proxy.match("~m POST ~u \"^http\:\/\/localhost\/mitm$\""):
  proxy.request.body.replace.file("./post.txt")
```


#### Disable the client cache and bypass the proxy cache
```python
if proxy.match("^https\:\/\/www.google.it\/$"):
  proxy.nocache()
  proxy.noproxycache(randomize_param="mynocache")
```

#### Add or replace an header
```python
if proxy.match("^https\:\/\/www.google.it\/$"):
  proxy.response.header.add("set-cookie", "proxy=1; max-age=31536000; expires=Tue, 07 Jun 2016 15:32:22 GMT;path=/; domain=.google.it;")
  proxy.response.header.replace("set-cookie", "proxy=1; max-age=31536000; expires=Tue, 07 Jun 2016 15:32:22 GMT;path=/; domain=.google.it;")
  proxy.request.header.add("Cookie", "proxy=1;")
  proxy.request.header.replace("Cookie", "proxy=2;")
```

#### Replace the content with an url
```python
if proxy.match("^https\:\/\/www.google.it\/$"):
  proxy.response.body.replace.url("http://www.bing.com/")
```

#### Replace in the original content using a regex
```python
if proxy.match("^https\:\/\/www.google.it\/$"):
  proxy.response.body.replace.regex("www\.google", "www.yahoo")	
```
#### Add or replace query parameters
```python
if proxy.match("^https\:\/\/www.google.it\/$"):
  proxy.response.query.add("proxy", "1")
  proxy.response.query.replace("proxy", "2")
```
#### Replace the host, port and path
```python
if proxy.match("^https\:\/\/www.google.it\/$"):
  proxy.request.host.replace("localhost") 
  proxy.request.port.replace(81)
  proxy.request.path.replace("/google.html")
```
#### Save the captured flow in a .har file
```python
proxy.savehar("./log.har")
```
