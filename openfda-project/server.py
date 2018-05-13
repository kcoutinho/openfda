import http.server
import socketserver
import http.client
import json

IP = "localhost"
PORT = 8000
socketserver.TCPServer.allow_reuse_address = True


class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    # GET
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        path=self.path

        def searching_drugs():

            headers = {'User-Agent': 'http-client'}
            conn = http.client.HTTPSConnection("api.fda.gov")
            components= path.strip("/search?").split("&")
            drug_comp = components[0].split("=")[1]

            if "limit" in path:
                limit = components[1].split("=")[1]
                if limit == "":
                    limit="20"
            else:
                limit="20"

            url = "/drug/label.json?search=active_ingredient:" + drug_comp + "limit=" + limit
            conn.request("GET", url, None, headers)
            r1 = conn.getresponse()
            print(r1.status, r1.reason)
            drugs_raw = r1.read().decode("utf-8")
            conn.close()
            drugs_repo = json.loads(drugs_raw)
            drugs_repo = drugs_repo['results']
            drugs = []
            n=0
            iterate = int(limit)
            beginning = "<!DOCTYPE html>" + "\n" + "<html>" + "\n" + "<ol>" + "\n"
            end = "</ul>" + "\n" + "</html>"
            while n < iterate:
                try:
                    drugs.append(drugs_repo[i]["openfda"]["brand_name"][0])
                    n += 1
                except:
                    drugs.append("Not known")
                    print("Any active ingredient has been assigned to this index")
                    n += 1

                with open('searchDrug.html', 'w') as f:
                    f.write(beginning)
                    drugs = str(drugs)
                    for drug in drugs:
                        drugs = "<t>" +"<li>" + drug
                        f.write(drugs)
                    f.write(end)

        def searching_companies():
            headers = {'id': 'http-client'}
            conn = http.client.HTTPSConnection("api.fda.gov")
            components = path.split("?")[1]
            company_comp = components.split("&")[0].split("=")[1]

            if "limit" in path:
                limit = components.split("&")[1].split("=")[1]
                if limit=="":
                    limit="20"
            else:
                limit="20"
            url = "/drug/label.json?search=company:" + company_comp + "&" + "limit=" + limit
            print(url)
            conn.request("GET", "/drug/label.json?", None, headers)
            r1 = conn.getresponse()
            company_raw = r1.read().decode("utf-8")
            conn.close()
            company_repo = json.loads(company_raw)
            company_repo = company_repo['results']
            companies = []
            iterate=int(limit)
            beginning = "<!DOCTYPE html>" + "\n" + "<html>" + "\n" + "<ol>" + "\n"
            end = "</ul>" + "\n" + "</html>"
            for i in range(0,iterate-1):
                if "manufacturer_name" in company_repo[i]:
                    companies.append(company_repo[i]["openfda"]["brand_name"][0])
                else:
                    companies.append("Any manufacturer has been assigned to this index")

            with open('searchCompany.html', 'w') as f:
                f.write(beginning)
                companies = str(companies)
                companies = "<li>" + companies + "</li>"
                f.write(companies)
                f.write(end)

        def listing_drugs():
            headers = {'User-Agent': 'http-client'}
            conn = http.client.HTTPSConnection("api.fda.gov")
            components = path.strip("label.json?").split("=")
            limit_drug = components[1]
            url = "/drug/label.json?limit=" + limit_drug
            conn.request("GET", url, None, headers)
            r1 = conn.getresponse()
            print(r1.status, r1.reason)
            drugs_info = r1.read().decode("utf-8")
            conn.close()
            drugs_info = json.loads(drugs_info)
            drugs_info = drugs_info["results"]
            drugs = []
            limit_int = int(limit_drug)
            for i in range(0, limit_int - 1):
                if "active_ingredient" in drugs_info[i]["active_ingredient"][0]:
                    drugs.append(drugs_info[i]["active_ingredient"][0])
                else:
                    drugs.append("Any active ingredient has been assigned to this index")
            with open('listDrugs.html', 'w') as f:
                f.write(beginning)
                for drug in drugs:
                    list_drugs = "<li>" + drug + "</li>"
                    f.write(list_drugs)
                f.write(end)
        def listing_companies():
            headers = {'id': 'http-client'}

            conn = http.client.HTTPSConnection("api.fda.gov")
            url = "/drug/label.json/listCompanies"
            conn.request("GET", url, None, headers)
            r1 = conn.getresponse()
            print(r1.status, r1.reason)
            repos_raw = r1.read().decode("utf-8")
            conn.close()
            repo = json.loads(repos_raw)
            repo = repo['results']
            companies = []
            for company in repo[0]['openfda']['manufacturer_name'[0]]:
                companies.append(company)

            with open('listCompany.html', 'w') as f:
                f.write(beginning)
                companies = str(companies)
                companies = "<li>" + companies + "</li>"
                f.write(companies)
                f.write(end)
        def listing_warnings():
            headers = {'User-Agent': 'http-client'}
            conn = http.client.HTTPSConnection("api.fda.gov")
            components = path.strip("label.json?").split("=")
            limit_warning = components[1]
            url = "/drug/label.json?limit=" + limit_warning
            conn.request("GET", url, None, headers)
            r1 = conn.getresponse()
            print(r1.status, r1.reason)
            warning_info = r1.read().decode("utf-8")
            conn.close()
            warning_info = json.loads(warning_info)
            warning_info = warning_info["results"]
            warnings = []
            limit_int = int(limit_warning)
            for i in range(0, limit_int - 1):
                if "active_ingredient" in warning_info[i]["active_ingredient"][0]:
                    warnings.append(warning_info[i]["active_ingredient"][0])
                else:
                    warnings.append("Any active ingredient has been assigned to this index")
            with open('listDrugs.html', 'w') as f:
                f.write(beginning)
                for warning in warnings:
                    list_warnings = "<li>" + warning + "</li>"
                    f.write(list_warnings)
                f.write(end)

        if path == "/":
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open("search.html", "r") as f:
                response = f.read()
                self.wfile.write(bytes(response, "utf8"))

        elif "searchDrug" in path:
            searching_drugs()
            with open('searchDrug.html','r') as f:
                response = f.read()
                self.wfile.write(bytes(response, "utf8"))


        elif "searchCompany" in path:
            searching_companies()
            with open('searchCompany.html','r') as f:
                response = f.read()
                self.wfile.write(bytes(response, "utf8"))

        elif "listDrugs" in path:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            listing_drugs()
            with open('listDrugs.html','r') as f:
                response = f.read()
                self.wfile.write(bytes(response, "utf8"))


        elif "listCompanies" in path:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            listing_companies()
            with open('listCompany.html', 'r') as f:
                response = f.read()
                self.wfile.write(bytes(response, "utf8"))
        elif "listWarnings" in path:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            listing_warnings()
            with open('listWarnings.html', 'r') as f:
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