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

        route = self.path #we rename the value of self.path to deal easier with the code
        #We establish the different possible options that can be found in the path and send an especific status
        if route == "/" or "searchDrug" in route or "searchCompany" in route or"listDrugs" in route or "listCompanies" in route or "listWarnings" in route:
            status_code = 200
        elif "redirect" in route:
            status_code = 302
        elif "secret" in route:
            status_code = 401
        else:
            status_code = 404
        self.send_response(status_code)

        #Taking into account the previous options if they are in the path, then the following headers are going to be sent:
        if route == "/" or "searchDrug" in route or "searchCompany" in route or "listDrugs" in route or "listCompanies" in route or "listWarnings" in route:
            self.send_header('Content-type', 'text/html')
        #According to the presence of some words in the path the components of the web are going to be established.
        elif "redirect" in route:
            self.send_header("Location","http://localhost:8000/")

        elif "secret" in route:
            self.send_header("WWW-Authenticate", "Basic realm='OpenFDA Private Zone'")
        self.end_headers()

        def searching_drugs(): #Searching_drugs is the first function created in this case with an empty argument. All the information related to the drugs that is relevant is goingto be stored inside of it

            headers = {'User-Agent': 'http-client'} #Headers
            conn = http.client.HTTPSConnection("api.fda.gov")
            components= route.strip("/search?").split("&") # /search? being deleted and the rest of the components of the url linked by &
            components_2 = components[0].split("=")[1]
            #This function supports a limit in order to let the client decide how many information he/she want to receive from the server.
            if "limit" in route:
                limit1 = components[1].split("=")[1]
                if limit1 == "":
                    limit1 = "10"
            else:
                limit1 = "10" #A limit of 10 is being predetermined.

            url = "/drug/label.json?search=active_ingredient:" + components_2 + "&" + "limit=" + limit1 #Construction of the elements that compose the url
            print(url)

            #To receive the data
            conn.request("GET", url, None, headers)
            r1 = conn.getresponse()
            print(r1.status, r1.reason)
            drugs_raw = r1.read().decode("utf-8")
            conn.close()
            drugs_repo = json.loads(drugs_raw)

            list_fda = [] #Building of an empty list
            n=0 #An element to iterate and that should start at 0
            iterate = int(limit1) #to iterate the limit is established as an integer
            message = "<head>" + "<h3>" + '<font face="verdana" size="4" color="black">' + "The brand names of the drugs searched are the corresponding following ones:" + "<body style='background-color:#FA8258'>"+ "</head>"+"<ol>"+"\n"
            #Doing iteration over the numbers until the limit
            while n < iterate:
                try:
                    list_fda.append(drugs_repo["results"][n]["openfda"]["brand_name"][0]) #Adding the desired information to the empty list created before
                    n += 1 #Add 1 to the value of n to continue iterating
                except: #Exception created to deal with situations in which the information is not avalaible
                    list_fda.append("Unknown")
                    print("Any active ingredient has been assigned to this index")
                    n += 1

            with open('searchDrugs.html', 'w') as doc: #A file is created to store the information that was obtained by the function
                doc.write(message)
                for drug in list_fda: #Iterating over the list to append each element to the file
                    list2 = "<t>" + "<li>" + drug
                    doc.write(list2)

        def searching_manufacturer_names():  # This is another function. In this case used to obtain information about manufacturers.
            #The process that was explained before is followed in this function too.
            headers = {'User-Agent': 'http-client'}
            conn = http.client.HTTPSConnection("api.fda.gov")
            components = route.strip("/search?").split("&")
            components_2 = components[0].split("=")[1]
            if "limit" in route:
                limit1 = components[1].split("=")[1]
                if limit1 == "":
                    limit1 = "10"
            else:
                limit1 = "10"

            url = "/drug/label.json?search=openfda.manufacturer_name:" + components_2 + "&" + "limit=" + limit1
            print(url)

            conn.request("GET", url, None, headers)
            r1 = conn.getresponse()
            print(r1.status, r1.reason)
            drugs_raw = r1.read().decode("utf-8")
            conn.close()
            drugs_repo = json.loads(drugs_raw)

            list_fda = []
            n = 0
            iterate = int(limit1)
            message = "<head>" + "<h3>" + '<font face="verdana" size="4" color="black">' + "The brand names of the drugs produced by the manufacturer are the corresponding following ones:" + "<body style='background-color:#FA8258'>" + "</head>""<ol>" + "\n"

            while n < iterate:
                try:
                    list_fda.append(drugs_repo["results"][n]["openfda"]["brand_name"][0])
                    n += 1
                except:
                    list_fda.append("Unknown")
                    print("The manufacturer name has not been found!")
                    n += 1

            with open('manufacturer_name.html', 'w') as doc:
                doc.write(message)
                for company in list_fda:
                    list2 = "<t>" + "<li>" + company
                    doc.write(list2)

        def listing_drugs(): #The process to build this function is also the same as the one that has been followed.
            #In this case the function is created to let the client obtain a list by given to the server a limit

            headers = {'User-Agent': 'http-client'}
            conn = http.client.HTTPSConnection("api.fda.gov")
            components = route.strip("/listDrugs?").split("=")
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
            message = "<head>" + "<h3>" + '<font face="verdana" size="4" color="black">' + "Here a list is shown with all the names of the companies required:" + "<body style='background-color:#F78181'>" + "</head>""<ol>" + "\n"
            iterate = int(limit)

            while n < iterate:
                try:
                    list_drugs.append(drugs_repo["results"][n]["openfda"]["brand_name"][0])
                    n += 1
                except:
                    list_drugs.append("Not known")
                    print("Any drug has been assigned to this index")
                    n += 1

            with open('listDrugs.html', 'w') as doc:
                doc.write(message)
                for drug in list_drugs:
                    list_drugs = "<t>" + "<li>" + drug
                    doc.write(list_drugs)


        def listing_manufacturers(): #A function to obtain a list related to manufacturers

            headers = {'User-Agent': 'http-client'}
            conn = http.client.HTTPSConnection("api.fda.gov")
            components = route.strip("/listCompanies?").split("=")
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
            message = "<head>" + "<h3>" + '<font face="verdana" size="4" color="black">' + "Here a list is shown with all the names of the companies required:" + "<body style='background-color:#F2F5A9'>" + "</head>""<ol>" + "\n"
            iterate = int(limit)

            while n < iterate:
                try:
                    list_companies.append(company_repo["results"][n]["openfda"]["manufacturer_name"][0])
                    n += 1
                except:
                    list_companies.append("Not known")
                    print("Any manufacturer has been assigned to this index")
                    n += 1

            with open('listCompanies.html', 'w') as doc:
                doc.write(message)
                for company in list_companies:
                    list_companies = "<t>" + "<li>" + company
                    doc.write(list_companies)

        def listing_warnings(): #A function to obtain information about warnings of drugs.

            headers = {'User-Agent': 'http-client'}
            conn = http.client.HTTPSConnection("api.fda.gov")
            components = route.strip("/listWarnings?").split("=")
            limit = components[1]
            url = "/drug/label.json?limit=" + limit
            print(url)
            conn.request("GET", url, None, headers)
            r1 = conn.getresponse()
            print(r1.status, r1.reason)
            warnings_raw = r1.read().decode("utf-8")
            conn.close()
            warnings_repo = json.loads(warnings_raw)
            list_warnings = []
            n = 0
            message = "<head>" + "<h3>" + '<font face="verdana" size="4" color="black">' + "Here a list is shown with all the names of the companies required:" + "<body style='background-color:#F2F5A9'>" + "</head>""<ol>" + "\n"
            iterate = int(limit)

            while n < iterate:
                try:
                    list_warnings.append(warnings_repo["results"][n]["warnings"][0])
                    n += 1
                except:
                    list_warnings.append("Not known")
                    print("Any warnings has been assigned to this index")
                    n += 1

            with open('listWarnings.html', 'w') as doc:
                doc.write(message)
                for warning in list_warnings:
                    list_warnings = "<t>" + "<li>" + warning
                    doc.write(list_warnings)


        if route == "/": #If the client doesn´t introduce an especific option in the path, automatically, the following message will be displayed
            try:
                print("SEARCH: The client is searching a web")
                with open("search.html", "r") as doc: #Then the file called search will be read by default.
                    response = doc.read()
                    self.wfile.write(bytes(response, "utf8")) #The response will be an html file with the corresponding information of search
            except KeyError:
                print("ERROR")
                print("Not found")
                with open("error.html","r") as doc:
                    response = doc.read()
                    self.wfile.write(bytes(response, "utf8"))

        elif 'searchDrug' in route: #If the client introduce this option in the path, the corresponding function will be called.
            searching_drugs() #The corresponding function will be called in order to be able to obtain its information.
            with open("searchDrugs.html","r") as doc: #The file related with the function will be opened to be read
                response = doc.read()
                self.wfile.write(bytes(response, "utf8")) #Finally the response will be an html display.

        #The same process will be followed by the different kind of options.
        elif "searchCompany" in route:
            searching_manufacturer_names()
            with open('manufacturer_name.html','r') as doc:
                response = doc.read()
                self.wfile.write(bytes(response, "utf8"))

        elif "listDrugs" in route:
            listing_drugs()
            with open('listDrugs.html','r') as doc:
                response = doc.read()
                self.wfile.write(bytes(response, "utf8"))

        elif "listCompanies" in route:
            listing_manufacturers()
            with open('listCompanies.html', 'r') as doc:
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
            print("Go back to the previous web page") #In this case the home page
            with open('search.html', 'r') as doc:
                response = doc.read()
                self.wfile.write(bytes(response, "utf8"))
        #In case that any of the previous options had been asked by the client, an error is going to be displayed.
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