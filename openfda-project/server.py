import http.server
import socketserver
import http.client
import json

IP = "localhost" #Localhost is referred to our own IP
PORT = 8000 #The predetermined port
socketserver.TCPServer.allow_reuse_address = True #This line of code is used in order to be able to reuse the port without any kind of error


class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler): #This class is going to be use to build the different components of the future response for the client
    # GET
    def do_GET(self):
        route = self.path
        if route == "/" or "searchDrug" in route or "searchCompany" in route or"listDrugs" in route or "listCompanies" in route or "listWarnings" in route:
            status_code = 200
        elif "redirect" in route:
            status_code = 302
        elif "secret" in route:
            status_code = 401
        else:
            status_code = 404
        self.send_response(status_code)
        if route == "/" or "searchDrug" in route or "searchCompany" in route or "listDrugs" in route or "listCompanies" in route or "listWarnings" in route:
            self.send_header('Content-type', 'text/html')
        elif "redirect" in route:
            self.send_header("Location","http://localhost:8000/")
        elif "secret" in route:
            self.send_header("WWW-Authenticate", "Basic realm='OpenFDA Private Zone'")
        self.end_headers()

        def searching_drugs():

            headers = {'User-Agent': 'http-client'}
            conn = http.client.HTTPSConnection("api.fda.gov")
            components= route.strip("/search?").split("&")
            drug_comp = components[0].split("=")[1]
            if "limit" in route:
                limit = components[1].split("=")[1]
                if limit == "":
                    limit = "15"
            else:
                limit = "15"

            url = "/drug/label.json?search=active_ingredient:" + drug_comp + "&" + "limit=" + limit
            print(url)

            conn.request("GET", url, None, headers)
            r1 = conn.getresponse()
            print(r1.status, r1.reason)
            drugs_raw = r1.read().decode("utf-8")
            conn.close()
            drugs_repo = json.loads(drugs_raw)

            drugs = []
            n=0
            iterate = int(limit)
            message = "<head>" + "<h3>" + '<font face="verdana" size="4" color="black">' + "The brand names of the drugs searched are the corresponding following ones:" + "<body style='background-color:#FA8258'>"+ "</head>"+"<ol>"+"\n"

            while n < iterate:
                try:
                    drugs.append(drugs_repo["results"][n]["openfda"]["brand_name"][0])
                    n += 1
                except:
                    drugs.append("Unknown")
                    print("Any active ingredient has been assigned to this index")
                    n += 1

            with open('searchDrug.html', 'w') as f:
                f.write(message)
                for drug in drugs:
                    drugs = "<t>" + "<li>" + drug
                    f.write(drugs)

        def searching_companies():
            headers = {'User-Agent': 'http-client'}
            conn = http.client.HTTPSConnection("api.fda.gov")
            components = route.strip("/search?").split("&")
            company_comp = components[0].split("=")[1]

            if "limit" in route:
                limit = components[1].split("=")[1]
                if limit == "":
                    limit = "15"
            else:
                limit = "15"

            url = "/drug/label.json?search=openfda.manufacturer_name:" + company_comp + "&" + "limit=" + limit
            print(url)

            conn.request("GET", url, None, headers)
            r1 = conn.getresponse()
            print(r1.status, r1.reason)
            company_raw = r1.read().decode("utf-8")
            conn.close()
            company_repo = json.loads(company_raw)

            companies = []
            n = 0
            iterate = int(limit)
            message = "<head>" + "<h3>" + '<font face="verdana" size="4" color="black">' + "The manufacturer names of the drugs searched are the corresponding following ones:" + "<body style='background-color:#81F79F'>" + "</head>""<ol>" + "\n"
            while n < iterate:
                try:
                    companies.append(company_repo["results"][n]["openfda"]["manufacturer_name"][0])
                    n += 1
                except:
                    companies.append("Unknown")
                    print("Any manufacturer name has been assigned to this index")
                    n += 1

            with open('searchCompany.html', 'w') as f:
                f.write(message)
                for company in companies:
                    companies = "<t>" + "<li>" + company
                    f.write(companies)

        def listing_drugs():

            headers = {'User-Agent': 'http-client'}
            conn = http.client.HTTPSConnection("api.fda.gov")
            components = route.strip("label.json?").split("=")
            limit = components[1]
            url = "/drug/label.json?limit=" + limit
            print(url)

            conn.request("GET", url, None, headers)
            r1 = conn.getresponse()
            print(r1.status, r1.reason)
            drugs_raw = r1.read().decode("utf-8")
            conn.close()
            drugs_repo = json.loads(drugs_raw)
            list_drugs = []
            n = 0
            iterate = int(limit)
            message = "<head>" + "<h3>" + '<font face="verdana" size="4" color="black">' + "Here a list is shown with all the names of the drugs required:" + "<body style='background-color:#F78181'>" + "</head>""<ol>" + "\n"
            while n < iterate:
                try:
                    list_drugs.append(drugs_repo["results"][n]["openfda"]["active_ingredient"][0])
                    n += 1
                except:
                    list_drugs.append("Unknown")
                    print("Any drug has been assigned to this index")
                    n += 1

            with open('listDrugs.html', 'w') as f:
                f.write(message)
                for drug in list_drugs:
                    list_drugs = "<t>" + "<li>" + drug
                f.write(list_drugs)

        def listing_companies():

            headers = {'User-Agent': 'http-client'}
            conn = http.client.HTTPSConnection("api.fda.gov")
            components = route.strip("label.json?").split("=")
            limit = components[1]
            url = "/drug/label.json?limit=" + limit
            print(url)
            conn.request("GET", url, None, headers)
            r1 = conn.getresponse()
            print(r1.status, r1.reason)
            company_raw = r1.read().decode("utf-8")
            conn.close()
            company_repo = json.loads(company_raw)
            list_companies = []
            n = 0
            iterate = int(limit)
            message = "<head>" + "<h3>" + '<font face="verdana" size="4" color="black">' + "Here a list is shown with all the names of the companies required:" + "<body style='background-color:#F2F5A9'>" + "</head>""<ol>" + "\n"
            while n < iterate:
                try:
                    list_companies.append(company_repo["results"][n]["openfda"]["manufacturer_name"][0])
                    n += 1
                except:
                    list_companies.append("Not known")
                    print("Any manufacturer has been assigned to this index")
                    n += 1

                with open('listCompanies.html', 'w') as f:
                    f.write(message)
                    for company in list_companies:
                        list_companies = "<t>" + "<li>" + company
                        f.write(list_companies)

        def listing_warnings():
            headers = {'User-Agent': 'http-client'}
            conn = http.client.HTTPSConnection("api.fda.gov")
            components = route.strip("label.json?").split("=")
            limit = components[1]
            url = "/drug/label.json?limit=" + limit
            print(url)

            conn.request("GET", url, None, headers)
            r1 = conn.getresponse()
            print(r1.status, r1.reason)
            warnings_raw = r1.read().decode("utf-8")
            conn.close()
            warning_repo = json.loads(warnings_raw)
            warnings=[]
            list_warnings = []
            n = 0
            m = 0
            ñ = 0
            iterate = int(limit)
            message = "<head>" + "<h3>" + '<font face="verdana" size="4" color="black">' + "Here a list is shown with all the warnings of drugs required:" + "<body style='background-color:#58FA58'>" + "</head>""<ol>" + "\n"
            while n < iterate:
                try:
                    warnings.append(warning_repo["results"][n]["openfda"]["brand_name"][0])
                    n += 1
                except:
                    warnings.append("Unknown")
                    n += 1
            while m < iterate:
                try:
                    list_warnings.append(warning_repo["results"][m]["warnings"][0])
                    n += 1
                except:
                    list_warnings.append("Unknown")
                    n += 1

                with open('listWarnings.html', 'w') as f:
                    f.write(message)
                    while ñ < iterate:
                        for warning in list_warnings:
                            list_warnings = "<t>" + "<li>" + warning
                            f.write(list_warnings)
                            ñ += 1

        if route == "/": #If the client doesn´t introduce an especific option in the path, automatically, the following message will be displayed
            try:
                print("SEARCH: The client is searching a web")
                with open("search.html", "r") as f: #Then the file called search will be read by default.
                    response = f.read()
                    self.wfile.write(bytes(response, "utf8")) #The response will be an html file with the corresponding information of search
            except KeyError:
                print("ERROR")
                print("Not found")
                with open("error.html","r") as doc:
                    response = doc.read()
                    self.wfile.write(bytes(response, "utf8"))

        elif 'searchDrug' in route: #If the client introduce this option in the path, the corresponding function will be called.
            searching_drugs() #The corresponding function will be called in order to be able to obtain its information.
            with open("searchDrug.html","r") as doc: #The file related with the function will be opened to be read
                response = doc.read()
                self.wfile.write(bytes(response, "utf8")) #Finally the response will be an html display.

        #The same process will be followed by the different kind of options.
        elif "searchCompany" in route:
            searching_companies()
            with open('searchCompany.html','r') as doc:
                response = doc.read()
                self.wfile.write(bytes(response, "utf8"))

        elif "listDrugs" in route:
            listing_drugs()
            with open('listDrugs.html','r') as doc:
                response = doc.read()
                self.wfile.write(bytes(response, "utf8"))

        elif "listCompanies" in route:

            listing_companies()
            with open('listCompany.html', 'r') as doc:
                response = doc.read()
                self.wfile.write(bytes(response, "utf8"))
        elif "listWarnings" in route:

            listing_warnings()
            with open('listWarnings.html', 'r') as doc:
                response = doc.read()
                self.wfile.write(bytes(response, "utf8"))

        elif "secret" in route:
            with open('secret.html', 'r') as doc:
                response = doc.read()
                self.wfile.write(bytes(response, "utf8"))
        elif "redirect" in route:
            print("Go back to the previous web page")
            with open('redirect.html', 'r') as doc:
                response = doc.read()
                self.wfile.write(bytes(response, "utf8"))
        else:
            print("ERROR")
            print("Not found")
            with open('error.html', 'r') as doc:
                response = doc.read()
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
print("")
print("Server stopped!")

# https://github.com/joshmaker/simple-python-webserver/blob/master/server.py