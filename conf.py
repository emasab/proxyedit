def init(proxy):
    pass
    #proxy.nocache()
    #proxy.noproxycache(randomize_param="kwnocache")

    if proxy.match("^https:\/\/social\.gelocal\.it\/social\/sites\/gelocal\/messaggeroveneto/loader.php?origin=MV_ACC_SLIM&mClose=2&backUrl=http%3A//m.messaggeroveneto.gelocal.it/udine&overwriteMClose=6&provider=facebook&rememberme=y.*"):
        proxy.response.body.replace.file("/home/emanuele/Desktop/loader.html")
    #if proxy.match("^http:\/\/webfragments\.repubblica\.it\/photogallery\/mobile\/2016-v2.*"):
    #    def red(context, flow):
    #        url = flow.request.url
    #        return url.replace("http://webfragments.repubblica.it/photogallery/mobile/2016-v1?", "http://192.168.1.100:81/workspace/dev-mi/cless/common/gallery/2016-v2/html/common/gallery.php?development=true&dev=mobile&collection=repubblica&")
    #    proxy.request.redirect(red)

    #if proxy.match("^http:\/\/test-webfragments\.repubblica\.it\/photogallery\/mobile\/2016-v2.*"):
    #    def red(context, flow):
    #        url = flow.request.url
    #        return url.replace("http://test-webfragments.repubblica.it/photogallery/mobile/2016-v2?", "http://192.168.1.100:81/workspace/dev-mi/cless/common/gallery/2016-v2/html/common/gallery.php?development=true&dev=mobile&collection=repubblica&")
    #    proxy.request.redirect(red)
    #proxy.response.header.delete("etag")

    #if proxy.match("~m POST"):
    #    proxy.request.body.log()
    #if proxy.match("https://www.repstatic.it/cless-mobile/main/amp/2016-v1/view/nazionale/detail.html"):
    #    proxy.response.body.replace.file("./content.html")
    #if proxy.match("https://oasjs.kataweb.it/amp/remote.html"):
    #    proxy.response.body.replace.file("./remote.html")
    # Replace a page with a local file
    #if proxy.match("^https\:\/\/www.google.it\/$"):
    #    proxy.response.body.replace.file("./content.html")

    # Replace request body
    #if proxy.match("~m POST ~u \"^http\:\/\/localhost:81\/mitm$\""):
    #    proxy.request.body.replace.file("./post.txt")

    # Disable client and bypass proxy cache
    #if proxy.match("^https\:\/\/www.google.it\/$"):
    #proxy.nocache()
    #proxy.noproxycache(randomize_param="kwnocache")


    # Add or replace an header
    #if proxy.match("^https\:\/\/www.google.it\/$"):
    #    proxy.response.header.add("set-cookie", "proxy=1; max-age=31536000; expires=Tue, 07 Jun 2016 15:32:22 GMT;path=/; domain=.google.it;")
    #    proxy.response.header.replace("set-cookie", "proxy=1; max-age=31536000; expires=Tue, 07 Jun 2016 15:32:22 GMT;path=/; domain=.google.it;")
    #    proxy.request.header.add("Cookie", "proxy=1;")
    #    proxy.request.header.replace("Cookie", "proxy=2;")

    # Replace the content with an url
    #if proxy.match("^https\:\/\/www.google.it\/$"):
    #    proxy.response.body.replace.url("http://www.bing.com/")


    # Replace in the original content using a regex
    #if proxy.match("^https\:\/\/www.google.it\/$"):
    #    proxy.response.body.replace.regex("www\.google", "www.yahoo")

    # Add or replace query parameters
    #if proxy.match("^https\:\/\/www.google.it\/$"):
    #    proxy.response.query.add("proxy", "1")
    #    proxy.response.query.replace("proxy", "2")

    # Replace the host, port and path
    #if proxy.match("^https\:\/\/www.google.it\/$"):
    #    proxy.request.host.replace("localhost")
    #    proxy.request.port.replace(81)
    #    proxy.request.path.replace("/google.html")

    # Save the captured flow in a .har file
    #proxy.savehar("./log.har")
