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
        if self.path == "/":
            with open("search.html", "r") as f:
                response=f.read()
                self.wfile.write(bytes(response, "utf8"))
        elif "search" in self.path:
            headers = {'id': 'http-client'}
            conn = http.client.HTTPSConnection("api.fda.gov")
            components= self.path.split("?")[1]
            drug= components.split("&")[0].split("=")[1]
            limit=components.split("&")[1].split("=")[1]
            url="/drug/label.json?search=active_ingredient:" + drug + "&" + "limit=" + limit
            print(url)
            conn.request("GET", "/drug/label.json?limit=10", None, headers)
            r1 = conn.getresponse()
            repos_raw = r1.read().decode("utf-8")
            conn.close()
            drugs =json.loads(repos_raw)
            drugs_li=str(drugs)
            self.wfile.write(bytes(drugs_li,"utf8"))


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