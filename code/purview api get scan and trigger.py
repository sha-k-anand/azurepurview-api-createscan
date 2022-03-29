import json
import requests
import os
import csv

purviewinstancename='zzazurepurview01'
tenantid='72f988bf-86f1-41af-91ab-2d7cd011db47'
purviewdatasourcename='SqlServer-MoF'

url = 'https://login.microsoftonline.com/'+ tenantid +'/oauth2/token'
myobj = {'client_id': '','client_secret': '','grant_type': 'client_credentials','resource': 'https://purview.azure.net'}
x = requests.post(url, data = myobj)
x1=  x.json()


mybearertoken = "Bearer " + x1["access_token"]

myheaders = {"Authorization":  mybearertoken }

print("----------------------------Data Sources-----------------------------------------------")
url = 'https://'+ purviewinstancename +'.scan.purview.azure.com/datasources?api-version=2018-12-01-preview'
listdatasources = requests.get(url,headers=myheaders)
print(listdatasources.json())
print("----------------------------Scans------------------------------------------------------")
url = 'https://'+ purviewinstancename +'.scan.purview.azure.com/datasources/'+ purviewdatasourcename +'/scans?api-version=2018-12-01-preview'
listdatasources = requests.get(url,headers=myheaders)
print(listdatasources.json())
print("-----------------------------Triggers---------------------------------------------------")
url = 'https://'+ purviewinstancename +'.scan.purview.azure.com/datasources/'+ purviewdatasourcename +'/scans/scandb01/triggers/default?api-version=2018-12-01-preview'
listdatasources = requests.get(url,headers=myheaders)
print(listdatasources.json())
print("-----------------------------Done------------------------------------------------------")



