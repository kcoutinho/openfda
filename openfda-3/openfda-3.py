import http.server
import socketserver
import http.client
import json
IP="localhost"
PORT = 8092

# HTTPRequestHandler class
class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    # GET
    def do_GET(self):
        # Send response status code
        self.send_response(200)

        # Send headers
        self.send_header('Content-type','text/html')
        self.end_headers()
        def

        def drugs_file(file_name):
            with open(file_name) as f:
                answer = f.read()
                self.wfile.write(bytes(answer,"utf8"))
        def drugs_list():
            headers = {'id': 'http-client'}
            conn = http.client.HTTPSConnection("api.fda.gov")
            conn.request("GET", "/drug/label.json?limit=10", None, headers)
            r1 = conn.getresponse()
            repos_raw = r1.read().decode("utf-8")
            conn.close()

        with open("drugs_html","w"):
            self.wfile.write(bytes())
            drugs = []
            for i in range(0, 10):
                message = drugs.append.repo[i]['id']

        repo = repo['results']


        # Write content as utf-8 data
            self.wfile.write(bytes(message, "utf8"))
            return

#Handler = http.server.SimpleHTTPRequestHandler
Handler = testHTTPRequestHandler

httpd = socketserver.TCPServer(("", PORT), Handler)
print("serving at port", PORT)
try:
    httpd.serve_forever()
except KeyboardInterrupt:
    pass
httpd.server_close()

# https://github.com/joshmaker/simple-python-webserver/blob/master/server.py