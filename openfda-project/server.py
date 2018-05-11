import http.server
import socketserver
import http.client
import json

IP = "localhost"
PORT = 8001
socketserver.TCPServer.allow_reuse_address = True

# HTTPRequestHandler class
class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    # GET
    def do_GET(self):
        headers = {'User-Agent': 'http-client'}
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

            conn = http.client.HTTPSConnection("api.fda.gov")
            drug_comp = path.split("&")[0].split("=")[1]
            limit = path.split("&")[1].split("=")[1]
            url="/drug/label.json?search=active_ingredient:" + drug_comp + "&" + "limit=" + limit
            conn.request("GET",url, None, headers)
            r1 = conn.getresponse()
            drugs_info = r1.read().decode("utf-8")
            conn.close()
            message = json.loads(drugs_info)
            drugs_info=drugs_info["results"]
            drugs=[]

            for i in range(drugs_info):
                if "active_ingredient" in drugs_info[i]:
                    drugs.append(drugs_info[i]["active_ingredient"][0])
                else:
                    drugs.append("Any active ingredient has been assigned to this index")
            print(drugs)


            with open('searchDrug.html','w') as f:
                f.write(beginning)
                drugs = str(drugs)
                for drug in drugs:
                    drugs = "<li>" + drug + "</li>"
                    f.write(drug)
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
            url = "/drug/label.json?search=company:" + company_comp + "&" + "limit=" + limit
            print(url)
            conn.request("GET","/drug/label.json?", None, headers)
            r1 = conn.getresponse()
            repos_raw = r1.read().decode("utf-8")
            conn.close()
            repo = json.loads(repos_raw)
            repo= repo['results']
            companies=[]

            for company in repo[0]['openfda']['manufacturer_name'[0]]:
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

            with open('listCompany.html', 'w') as f:
                f.write(beginning)
                companies = str(companies)
                companies = "<li>" + companies + "</li>"
                f.write(companies)
                f.write(end)
            with open('listCompany.html', 'r') as f:
                response = f.read()
                self.wfile.write(bytes(response, "utf8"))

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