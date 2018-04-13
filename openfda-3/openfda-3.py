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


        headers = {'id': 'http-client'}

        conn = http.client.HTTPSConnection("api.fda.gov")
        conn.request("GET", "/drug/label.json?limit=10", None, headers)
        r1 = conn.getresponse()
        repos_raw = r1.read().decode("utf-8")
        conn.close()
        repo = json.loads(repos_raw)

        repo = repo['results']
        drugs=[]
        for i in range(0,10):
            message=drugs.append.repo[i]['id']

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