import http.server
import cgi
import time

class MyHTTPRequestHandler (http.server.BaseHTTPRequestHandler) :
    def do_GET (self) :
        self.send_response (200)
        self.send_header ('Content-type', 'text/html')
        self.end_headers ()
        f = open ("index.html", "rb")
        self.wfile.write (f.read ())
    def do_POST (self) :
        self.send_response (200)
        self.send_header ('Content-type', 'text/html')
        self.end_headers()
        header = self.headers.get('content-type')
        # print (self.headers.keys ())
        # print (header)
        # print ("####")
        ctype, pdict = cgi.parse_header (header)
        # this type conversion is because parse_multipart wants a binary thing for some reason
        pdict ['boundary'] = bytes ( pdict ['boundary'], "utf-8" )
        form = cgi.parse_multipart (self.rfile, pdict)
        fml = form ['myfile'] [0]
        #print (form)
        with open("upload/{}".format(time.time_ns()), 'wb') as f :
            f.write (fml)

httpd = http.server.HTTPServer (('0.0.0.0', 8000), MyHTTPRequestHandler)
httpd.serve_forever ()
