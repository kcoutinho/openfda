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

        beginning = "<!DOCTYPE html>" + "\n" + "<html>" + "\n" + "<ol>" + "\n"
        end = "</ul>" + "\n" + "</html>"

        if path == "/":
            with open("html_response.html", "r") as f:
                response = f.read()
                self.wfile.write(bytes(response, "utf8"))

        elif "searchDrug" in path:
            headers = {'id': 'http-client'}
            conn = http.client.HTTPSConnection("api.fda.gov")
            components = self.path.split("?")[1]
            drug_comp = components.split("&")[0].split("=")[1]
            limit = components.split("&")[1].split("=")[1]
            conn.request("GET","/drug/label.json?search=active_ingredient:" + drug_comp + "&" + "limit=" + limit, None, headers)
            r1 = conn.getresponse()
            repos_raw = r1.read().decode("utf-8")
            conn.close()
            repo = json.loads(repos_raw)
            repo = repo['results']
            drugs=[]

            for drug in repo[0]['active_ingredient'][0]:
                drugs.append(drug)

            with open('searchDrug.html','w') as f:
                f.write(beginning)
                drugs=str(drugs)
                drugs= "<li>" + drugs + "</li>"
                f.write(drugs)
                f.write(end)
            with open('searchDrug.html','r') as f:
                response = f.read()
                self.wfile.write(bytes(response, "utf8"))



        elif "searchCompany" in path:
            headers = {'id': 'http-client'}
            conn = http.client.HTTPSConnection("api.fda.gov")
            components = self.path.split("?")[1]
            company_comp = components.split("&")[0].split("=")[1]
            limit = components.split("&")[1].split("=")[1]
            conn.request("GET","/drug/label.json?search=company_name:" + company_comp + "&" + "limit=" + limit, None, headers)
            r1 = conn.getresponse()
            repos_raw = r1.read().decode("utf-8")
            conn.close()
            repo = json.loads(repos_raw)
            repo= repo['results']
            companies=[]

            for company in repo[0]['active_ingredient'][0]:
                companies.append(company)

            with open('searchCompany.html','w') as f:
                f.write(beginning)
                companies=str(companies)
                companies= "<li>" + companies + "</li>"
                f.write(companies)
                f.write(end)
            with open('searchCompany.html','r') as f:
                response = f.read()
                self.wfile.write(bytes(response, "utf8"))

        elif "listDrugs" in path:
            headers = {'id': 'http-client'}

            conn = http.client.HTTPSConnection("api.fda.gov")
            conn.request("GET", "/drug/label.json/listDrugs", None, headers)
            r1 = conn.getresponse()
            print(r1.status, r1.reason)
            repos_raw = r1.read().decode("utf-8")
            conn.close()
            repo = json.loads(repos_raw)
            drugs=[]

            for drug in repo[0]['active_ingredient'][0]:
                drugs.append(drug)


            with open('listDrugs.html','w') as f:
                f.write(beginning)
                drugs=str(drugs)
                drugs= "<li>" + drugs + "</li>"
                f.write(drugs)
                f.write(end)
            with open('listDrugs.html','r') as f:
                response = f.read()
                self.wfile.write(bytes(response, "utf8"))

        elif "listCompanies" in path:
            headers = {'id': 'http-client'}

            conn = http.client.HTTPSConnection("api.fda.gov")
            conn.request("GET", "/drug/label.json/listCompanies", None, headers)
            r1 = conn.getresponse()
            print(r1.status, r1.reason)
            repos_raw = r1.read().decode("utf-8")
            conn.close()
            repo = json.loads(repos_raw)
            repo = repo['results']
            companies=[]
            for company in repo[0]['openfda']['manufacturer_name'[0]]:
                companies.append(company)

            with open('searchCompany.html', 'w') as f:
                f.write(beginning)
                companies = str(companies)
                companies = "<li>" + companies + "</li>"
                f.write(companies)
                f.write(end)
            with open('searchCompany.html', 'r') as f:
                response = f.read()
            self.wfile.write(bytes(response, "utf8"))

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