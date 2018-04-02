import http.client
import json

headers = {'id': 'http-client'}

conn = http.client.HTTPSConnection("api.fda.gov")
conn.request("GET", '/drug/label.json?limit=20', None, headers)
r1 = conn.getresponse()
print(r1.status, r1.reason)
repos_raw = r1.read().decode("utf-8")
conn.close()
repo = json.loads(repos_raw)
repo = repo['results']
for i in range(0,20):
    if "Salicylic acid" in repo[i]['active_ingredient'][0]:
        print("The manufacturer name of the drug",i+1,"is:",repo[i]['openfda']['manufacturer_name'][0])
    else:
        continue