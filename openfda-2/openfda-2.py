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
active_ingredient = [repo[0]['active_ingredient']]
print(active_ingredient)
for number in range(0,20):
    if "Salicylic acid" in repo[number]['active_ingredient'][0]:
        print("The manufacturer name of the drug",number+1,"is:",repo[number]['openfda']['manufacturer_name'][0])