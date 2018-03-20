import http.client
import json

headers = {'id': 'http-client'}

conn = http.client.HTTPSConnection("api.fda.gov")
conn.request("GET", "/drug/label.json", None, headers)
r1 = conn.getresponse()
print(r1.status, r1.reason)
repos_raw = r1.read().decode("utf-8")
conn.close()
repo = json.loads(repos_raw)
print(repo)
print("The total number of repos of this user is:", len(repo))


repo = repo['results']
print("The id of the drug is", repo[0]['id'])
print("The purpose of the drug is", repo[0]['purpose'])
print("The manufacturer name of the drug is", repo[0]['openfda']['manufacturer_name'])