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
        print ("header:")
        print (header)
        print ("pdict:")
        print (pdict)
        print ("rfile:")
        print (self.rfile)

        # get file names
        # because cgi.parse_multipart doesn't do it
        stri = self.rfile.peek()
        print (stri)
        name_getting_boundary = "--" + pdict ['boundary']
        name_getting_boundary = bytes(name_getting_boundary, "utf-8")
        # filenames does not contain file names yet
        # but we're getting there
        filenames = stri.split(name_getting_boundary)
        filenames.remove(b'')
        filenames.remove(b'--\r\n')
        for i, filebytes in enumerate(filenames):
            filestring = filebytes.decode("utf-8")
            name_beginning = filestring.find('filename') + 10
            name_end = filestring.find('"', name_beginning)
            filename = filebytes[name_beginning:name_end].decode("utf-8")
            # print(filename)
            filenames[i] = filename
        print (filenames)

        # get the file contents and save each file
        # this type conversion is because parse_multipart wants a binary thing for some reason
        pdict ['boundary'] = bytes ( pdict ['boundary'], "utf-8" )
        form = cgi.parse_multipart (self.rfile, pdict)
        for i, fml in enumerate(form['myfile']):
            with open("upload/{}".format(filenames[i]), 'wb') as f:
                f.write(fml)

httpd = http.server.HTTPServer (('0.0.0.0', 8000), MyHTTPRequestHandler)
httpd.serve_forever ()
