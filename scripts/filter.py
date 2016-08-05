# Usage: mitmdump -s "modify_response_body.py mitmproxy bananas"
# (this script works best with --anticache)
import os, sys, re, time, hashlib, random
sys.path.append(".")
sys.path.append("./scripts")
import har_extractor
import conf
from urllib2 import urlopen
from mitmproxy.script import concurrent
from mitmproxy.models import HTTPResponse
from netlib.http import Headers

class Match(object):

    def match(self, proxy, m):
        ProxyConf.set_match(m)
        return True


class NoProxyCache(object):

    def noproxycache(self, proxy, debugger_friendly = False, randomize_param=False):
        def val(context, flow):
            if not debugger_friendly:
                val = str(int(time.time()*1000))
            else:
                val = flow.original.request.headers["Referer"]
                if len(val)==0:
                    val = [flow.original.request.url]
                val = hashlib.sha256(val[0]).hexdigest()
                val = val[len(val)-10:]

            return val

        param = "nocache"
        if randomize_param is True:
            param = ''.join(random.choice('0123456789ABCDEF') for i in range(10))
        elif not randomize_param is False:
            param = randomize_param

        proxy.request.header.delete("If-None-Match", True)
        proxy.request.header.delete("If-Modified-Since", True)
        proxy.request.query.replace(param, val)

class ProxyConf(dict):

    _match = "all"
    _extensions = []

    @classmethod
    def set_match(cls, m):
        ProxyConf._match = m


    @classmethod
    def get_extension_method(cls, proxy, m):
        for e in ProxyConf._extensions:
            if hasattr(e,m):
                return lambda *args,  **kwds: getattr(e,m)(proxy, *args, **kwds)
        return None

    @classmethod
    def add_extension(cls, e):
        ProxyConf._extensions.append(e)

    def __init__(self, parent = None, key = None):
        self.parent = parent
        self.key = key
        self.base = parent is None


    def _get_dict(self):
        match = ProxyConf._match
        if self.base:
            if not match in self:
                self[match] = ProxyConf(self, match)
            cD = self[match]
        else:
            cD = self
        return cD

    def __getattr__(self, attr):
        if self.base:
            ext1 = ProxyConf.get_extension_method(confDict, attr)
            if not ext1 is None:
                return ext1

        cD = self._get_dict()

        if not attr in cD:
            cD[attr] = ProxyConf(cD, attr)

        return cD[attr]

    def __call__(self, *args):
        cD = self._get_dict()

        if len(args)<2:
            if len(args)==0:
                v = True
            else:
                v = args[0]
            self.parent[self.key] = v
        elif len(args)==2:
            cD[args[0]] = args[1]


confDict = ProxyConf()
ProxyConf.add_extension(Match())
ProxyConf.add_extension(NoProxyCache())
conf.init(confDict)
conf = confDict
print(conf)

def nocache(flow):
    flow.response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, max-age=0"


def realv(v, context, flow):
    if callable(v):
        return v(context, flow)
    else:
        return v

def process_headers(flow, headers, direction):
    if direction == "REQUEST":
        flow_dir = flow.request
    else:
        flow_dir = flow.response

    changed_h = False
    if "add" in headers:
        headers = headers["add"]
        for k,v in headers.items():
            flow_dir.headers[k] = realv(v, context, flow)
            changed_h = True
            print("\nADDED %s HEADER: %s\n" % (direction,k))


    if "replace" in headers:
        headers = headers["replace"]
        for k,v in headers.items():
            if k in flow_dir.headers:
                del flow_dir.headers[k]
            flow_dir.headers[k] = realv(v, context, flow)
            changed_h = True
            print("\nREPLACED %s HEADER: %s\n" % (direction,k))

    if "delete" in headers:
        headers = headers["delete"]
        for d in headers:
            if d in flow_dir.headers:
                del flow_dir.headers[d]
            changed_h = True
            print("\nDELETED %s HEADER: %s\n" % (direction,d))

    return changed_h

def process_body(flow, body, direction):
    if direction == "REQUEST":
        flow_dir = flow.request
    else:
        flow_dir = flow.response

    if "replace"in body:
        body = body["replace"]
        for k,v in body.items():
            if k == "file":
                body1 = open(v).read()
                flow_dir.content = body1
                print("\nREPLACED %s BODY WITH FILE: %s\n" % (direction,v))
            elif k == "url":
                body1 = urlopen(v).read()
                flow_dir.content = body1
                print("\nREPLACED %s BODY WITH URL: %s\n" % (direction,v))
            elif k == "regex":
                for k,v in body["regex"].items():
                    flow_dir.content = re.sub(k,v,flow_dir.content)
                    print("\nREPLACED %s BODY WITH REGEXP: %s\n" % (direction,k))

@concurrent
def request(context, flow):
    direction = "REQUEST"
    q = flow.request.get_query()
    flow.original = flow.copy()
    original = flow.original

    changed_q = False
    changed_h = False
    changed_host = False
    changed_path = False
    for k in conf.keys():
        conf1 = conf[k]

        escape_match = False
        try:
            escape_match = original.match(re.escape(k))
        except Exception as e:
            pass

        if k == "all" or escape_match or k and original.match(k):

            if "request" in conf1 and "path" in conf1["request"]:
                path = conf1["request"]["path"]
                if "replace" in path:
                    path = path["replace"]
                    flow.request.path = realv(path, context, flow)
                    changed_path = True

            if "request" in conf1 and "protocol" in conf1["request"]:
                protocol = conf1["request"]["protocol"]
                if "replace" in protocol:
                    protocol = protocol["replace"]
                    flow.request.protocol = realv(protocol, context, flow)

            if "request" in conf1 and "port" in conf1["request"]:
                port = conf1["request"]["port"]
                if "replace" in port:
                    port = port["replace"]
                    flow.request.port = realv(port, context, flow)


            if "request" in conf1 and "host" in conf1["request"]:
                host = conf1["request"]["host"]
                if "replace" in host:
                    host = host["replace"]
                    flow.request.host = realv(host, context, flow)
                    changed_host = True


            if "request" in conf1 and "query" in conf1["request"]:
                query = conf1["request"]["query"]
                if "replace" in query:
                    query = query["replace"]
                    for k,v in query.items():
                        q[k] = [realv(v, context, flow)]
                        changed_q = True

            if "request" in conf1 and "redirect" in conf1["request"]:
                redirect = conf1["request"]["redirect"]
                redirect = realv(redirect, context, flow)
                resp = HTTPResponse(
                        b"HTTP/1.1", 302, b"OK",
                        Headers(Location=redirect.encode('utf-8')),
                        b""
                    )
                flow.reply(resp)

            if "request" in conf1 and "header" in conf1["request"]:

                headers = conf1["request"]["header"]

                changed_h = changed_h or process_headers(flow, headers, direction)

            if "request" in conf1 and "body" in conf1["request"]:

                body = conf1["request"]["body"]
                process_body(flow, body, direction)



    if changed_q:
        flow.request.set_query(q)
    if changed_h:
        print(flow.request.headers)
    if changed_host:
        flow.request.update_host_header()


@concurrent
def response(context, flow):
    direction = "RESPONSE"
    if "all" in conf and "nocache" in conf["all"]:
        nocache(flow)

    has_resp = len([ 1 for v in conf.values() if "response" in v or "nocache" in v ])>0
    if has_resp:
        original = flow.original
        original_resp = flow.response.copy()

        for k in conf.keys():
            conf1 = conf[k]
            if "nocache" in conf1:
                nocache(flow)

        escape_match = False
        try:
            escape_match = original.match(re.escape(k))
        except Exception as e:
            pass


        if k == "all" or escape_match or original.match(k):

            if "response" in conf1:
                if "header" in conf1["response"]:
                    headers = conf1["response"]["header"]
                    process_headers(flow, headers, direction)

                if "body" in conf1["response"]:
                    body = conf1["response"]["body"]
                    process_body(flow, body, direction)

    har_extractor.response(context,flow)

def start(context, argv):
    if "all" in conf and "savehar" in conf["all"]:
        savehar = conf["all"]["savehar"]
        har_extractor.start(context, savehar)

def done(context):
    har_extractor.done(context)
