import http.server
import socketserver
import http.client
import json
socketserver.TCPServer.allow_reuse_adress = True
IP="localhost"
PORT = 8000

# HTTPRequestHandler class
class openfda(http.server.BaseHTTPRequestHandler):
    # GET
    def do_GET(self):
        # Send response status code
        self.send_response(200)
        # Send headers
        self.send_header('Content-type','text/html')
        self.end_headers()

    headers = {'id': 'http-client'}

    conn = http.client.HTTPSConnection("api.fda.gov")
    conn.request("GET", "/drug/label.json", None, headers)
    r1 = conn.getresponse()
    print(r1.status, r1.reason)
    repos_raw = r1.read().decode("utf-8")
    conn.close()
    repo = json.loads(repos_raw)
    repo = repo['results']
    def searchDrug(self, drug):
        drugs=[]
        for element in drug:
            for drug in repo["patient"]["drug"]





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