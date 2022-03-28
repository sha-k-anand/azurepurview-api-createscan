
from email import header
import json
import requests
import os
import csv

url = 'https://login.microsoftonline.com/{replacetenantid}/oauth2/token'
myobj = {'client_id': '','client_secret': '','grant_type': 'client_credentials','resource': 'https://purview.azure.net'}
x = requests.post(url, data = myobj)
x1=  x.json()

#{'token_type': 'Bearer', 'expires_in': '86399', 'ext_expires_in': '86399', 'expires_on': '1648325241', 'not_before': '1648238541', 'resource': 'https://purview.azure.net', 'access_token': ''}
#x1= json.dumps(x.text)
#print(x1["token_type"])

mybearertoken = "Bearer " + x1["access_token"]

#myheaders = {"Authorization": "Bearer MYREALLYLONGTOKENIGOT"}
myheaders = {"Authorization":  mybearertoken }

url = 'https://zzazurepurview01.scan.purview.azure.com/datasources?api-version=2018-12-01-preview'
listdatasources = requests.get(url,headers=myheaders)
#print(listdatasources.json())

#https://zzazurepurview01.scan.purview.azure.com/datasources/SqlServer-MoF/scans/Scan-3aS?api-version=2018-12-01-preview

mydata={
    "properties": {
        "credential": {
            "referenceName": "cred",
            "credentialType": "SqlAuth"
        },
        "serverEndpoint": "WINDEV2112EVAL\\\SK1",
        "databaseName": "AdventureWorks2019z2",
        "scanRulesetName": "SqlServer",
        "scanRulesetType": "System",
        "collection": {
            "referenceName": "zzazurepurview01",
            "type": "CollectionReference"
        },
            "connectedVia": {
            "referenceName": "IntegrationRuntime-Quc",
            "integrationRuntimeType": "SelfHosted"
        }
    },
    "kind": "SqlServerDatabaseCredential"
}

infile_folder = "C:\\purview apis\\scanlist.txt"
scanname=""
dbname=""

myheaders = {"Authorization":  mybearertoken }


with open(infile_folder) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter='|')
    line_count = 0
    for row in csv_reader:
        scanname = row[0]
        dbname = row[1]
        print(f'\t{row[0]} | {row[1]} ')
        line_count += 1

        mydata='{    "properties": {        "credential": {            "referenceName": "cred",            "credentialType": "SqlAuth"        },        "recurrenceInterval": null,        "serverEndpoint": "WINDEV2112EVAL\\\SK1",        "databaseName": "'+ dbname +'",        "scanRulesetName": "SqlServer",        "scanRulesetType": "System",        "collection": {            "referenceName": "zzazurepurview01",            "type": "CollectionReference"        },            "connectedVia": {            "referenceName": "IntegrationRuntime-Quc",            "integrationRuntimeType": "SelfHosted"        }    },    "kind": "SqlServerDatabaseCredential"}'
        mydata1=json.loads(mydata)
        url = 'https://zzazurepurview01.scan.purview.azure.com/datasources/SqlServer-MoF/scans/'+ scanname +'?api-version=2018-12-01-preview'
        out=requests.put(url,json=mydata1,headers=myheaders)
        print(out.json())

        mydata1='{"properties": {"recurrence": {"frequency": "Month","interval": 1,"startTime": "2022-03-25T02:04:00Z", "endTime": null,"schedule": {"minutes": [0],"hours": [7],"weekDays": null,"monthDays": [2],"monthlyOccurrences": null},"timezone": "UTC"},"recurrenceInterval": null,"createdAt": "2022-03-25T02:06:02.5748139Z","lastModifiedAt": "2022-03-25T02:06:02.5748139Z","lastScheduled": null,"scanLevel": "Incremental" },"name": "default"}'
        mydata1=json.loads(mydata)
        url = 'https://zzazurepurview01.scan.purview.azure.com/datasources/SqlServer-MoF/scans/'+ scanname +'/triggers/default?api-version=2018-12-01-preview'
        out=requests.put(url,json=mydata1,headers=myheaders)
        print(out.json())


    print(f'Processed {line_count} lines.')




print("Done")

