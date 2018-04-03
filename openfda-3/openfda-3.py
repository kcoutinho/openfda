PORT=8000
class testHTTPRequestHandler(http.server.BaseHTTPRequest.Handler):
    def do_GET(self):
self.send_response(200)
self.end_headers()