import json
import requests
import os
import csv

purviewinstancename='zzazurepurview01'
tenantid='72f988bf-86f1-41af-91ab-2d7cd011db47'

url = 'https://login.microsoftonline.com/'+ tenantid +'/oauth2/token'
myobj = {'client_id': '','client_secret': '','grant_type': 'client_credentials','resource': 'https://purview.azure.net'}
x = requests.post(url, data = myobj)
x1=  x.json()

mybearertoken = "Bearer " + x1["access_token"]

myheaders = {"Authorization":  mybearertoken }
#https://docs.microsoft.com/en-us/rest/api/purview/scanningdataplane/data-sources/create-or-update?tabs=HTTP

url = 'https://'+ purviewinstancename +'.scan.purview.azure.com/datasources?api-version=2022-02-01-preview'
listdatasources = requests.get(url,headers=myheaders)
print(listdatasources.json())
print("----------------------------------------------------------")


myheaders = {"Authorization":  mybearertoken }

mydata = '{"properties": {"serverEndpoint": "shakasqlserver0001.database.windows.net",        "resourceGroup": "sqlserver001",        "subscriptionId": "c8ae7563-2954-4307-b209-e472425469f4",        "location": "southcentralus",        "resourceName": "shakasqlserver0001",        "resourceId": "/subscriptions/c8ae7563-2954-4307-b209-e472425469f4/resourceGroups/sqlserver001/providers/Microsoft.Sql/servers/shakasqlserver0001",        "dataUseGovernance": "Disabled", "collection": { "lastModifiedAt": "2022-08-08T14: 40: 29.5108053Z", "referenceName": "zzazurepurview01",  "type": "CollectionReference"        },        "dataSourceCollectionMovingState": 0    },    "kind": "AzureSqlDatabase",    "id": "datasources/AzureSqlDatabase-AHQ",    "name": "AzureSqlDatabase-AHQ"}'
purviewdatasourcename='azscan01'

mydata1=json.loads(mydata)
url = 'https://'+ purviewinstancename +'.scan.purview.azure.com/datasources/'+ purviewdatasourcename +'?api-version=2022-02-01-preview'
out=requests.put(url,json=mydata1,headers=myheaders)
print(out.json())
print("Done")
