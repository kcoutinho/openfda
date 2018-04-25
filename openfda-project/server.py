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

        path= self.path

        if path == "/":
            with open("html_response.html", "r") as f:
                response = f.read()
                self.wfile.write(bytes(response, "utf8"))
        headers = {'id': 'http-client'}
        conn = http.client.HTTPSConnection("api.fda.gov")
        components = self.path.split("?")[1]
        elif "searchDrug" in path:
            drug_comp = components.split("&")[0].split("=")[1]
            limit = components.split("&")[1].split("=")[1]
            conn.request("GET","/drug/label.json?search=active_ingredient:" + drug_comp + "&" + "limit=" + limit, None, headers)
            r1 = conn.getresponse()
            repos_raw = r1.read().decode("utf-8")
            conn.close()
            drugs = json.loads(repos_raw)
            drugs_li = str(drugs)
            self.wfile.write(bytes(drugs_li, "utf8"))
        elif "searchCompany" in path:
            company_comp = components.split("&")[0].split("=")[1]
            limit = components.split("&")[1].split("=")[1]
            conn.request("GET","/drug/label.json?search=company_name:" + company_comp + "&" + "limit=" + limit, None, headers)
            r1 = conn.getresponse()
            repos_raw = r1.read().decode("utf-8")
            conn.close()
            companies = json.loads(repos_raw)
            companies_li = str(companies)
            self.wfile.write(bytes(drugs_li, "utf8"))
        elif "listDrugs" in path:



    def searchDrug(self, drug):
        conn = http.client.HTTPSConnection("api.fda.gov")
        conn.request("GET", "/drug/label.json", None, headers)
        r1 = conn.getresponse()
        print(r1.status, r1.reason)
        repos_raw = r1.read().decode("utf-8")
        conn.close()
        repo = json.loads(repos_raw)
        repo = repo['results']
        drugs=[]
        for element in drug:
            for drug in repo[0]['active_ingredient'][0]:
                drugs.append(drug)
        return drugs

    def searchCompany(self,company):
        conn = http.client.HTTPSConnection("api.fda.gov")
        conn.request("GET", "/drug/label.json", None, headers)
        r1 = conn.getresponse()
        print(r1.status, r1.reason)
        repos_raw = r1.read().decode("utf-8")
        conn.close()
        repo = json.loads(repos_raw)
        repo = repo['results']
        companies = []
        for element in company:
            for company in repo[0]['openfda']['manufacturer_name']:
                companies.append(company)
        return companies







            return

#Handler = http.server.SimpleHTTPRequestHandler
Handler = openfda

httpd = socketserver.TCPServer(("", PORT), Handler)
print("serving at port", PORT)
try:
    httpd.serve_forever()
except KeyboardInterrupt:
    pass
httpd.server_close()

# https://github.com/joshmaker/simple-python-webserver/blob/master/server.py