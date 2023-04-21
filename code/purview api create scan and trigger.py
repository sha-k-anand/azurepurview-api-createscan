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

#{'token_type': 'Bearer', 'expires_in': '86399', 'ext_expires_in': '86399', 'expires_on': '1648325241', 'not_before': '1648238541', 'resource': 'https://purview.azure.net', 'access_token': ''}
#x1= json.dumps(x.text)
#print(x1["access_token"])

mybearertoken = "Bearer " + x1["access_token"]

myheaders = {"Authorization":  mybearertoken }

url = 'https://'+ purviewinstancename +'.scan.purview.azure.com/datasources?api-version=2018-12-01-preview'
listdatasources = requests.get(url,headers=myheaders)
#print(listdatasources.json())

#https://zzazurepurview01.scan.purview.azure.com/datasources/SqlServer-MoF/scans/Scan-3aS?api-version=2018-12-01-preview

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
        recurrenceperiod=row[2]
        scanhour=row[3]
        scanminute=row[4]
        scanday=row[5]
        print(f'\t{row[0]} | {row[1]} ')

        print(f'Submitting Scan for {scanname}... Started')
        #mydata=  '{    "properties": {        "credential": {            "referenceName": "cred",            "credentialType": "SqlAuth"        },        "recurrenceInterval": null, "serverEndpoint": "WINDEV2112EVAL\\\SK1",        "databaseName": "'+ dbname +'",        "scanRulesetName": "SqlServer",        "scanRulesetType": "System",        "collection": {            "referenceName": "zzazurepurview01",            "type": "CollectionReference"        },            "connectedVia": {            "referenceName": "IntegrationRuntime-Quc",            "integrationRuntimeType": "SelfHosted"        }    },    "kind": "SqlServerDatabaseCredential"}'
        mydata = '{    "properties": {        "credential": {            "referenceName": "azpurviewstgsvc", "credentialType": "SqlAuth"        },        "recurrenceInterval": null, "serverEndpoint": "S01VSSSQLCL001\\\Shore1",     "databaseName": "'+ dbname +'",        "scanRulesetName": "SqlServer",        "scanRulesetType": "System",        "collection": {            "referenceName": "5tqycb",                      "type": "CollectionReference"        },            "connectedVia": {            "referenceName": "IntegrationRuntime-S01VDSPVIEW002", "integrationRuntimeType": "SelfHosted"        }    },    "kind": "SqlServerDatabaseCredential"}'


        mydata1=json.loads(mydata)
        url = 'https://'+ purviewinstancename +'.scan.purview.azure.com/datasources/'+ purviewdatasourcename +'/scans/'+ scanname +'?api-version=2018-12-01-preview'
        out=requests.put(url,json=mydata1,headers=myheaders)
        #print(out.json())
        print(f'Submitting Scan for {scanname}... Completed')
        print()

        print(f'Submitting Trigger for {scanname}... Started')
        mydata='{  "properties": {    "recurrenceInterval": null,    "scanLevel": "Incremental",    "recurrence": {      "startTime": "2022-03-28T14:59:00.416Z",      "endTime": "2023-03-25T00:00:00.000Z",      "interval": 1,      "frequency": "Month",      "schedule": {        "hours": [          ' + scanhour +'        ],        "minutes": [          '+ scanminute +'        ],        "monthDays": [          '+ scanday +'        ]      }    }  }} '
        mydata1=json.loads(mydata)
        url = 'https://'+ purviewinstancename +'.scan.purview.azure.com/datasources/'+ purviewdatasourcename +'/scans/'+ scanname +'/triggers/default?api-version=2018-12-01-preview'
        out=requests.put(url,json=mydata1,headers=myheaders)
        #print(out.json())
        print(f'Submitting Trigger for {scanname}... Completed')
        line_count += 1


    print(f'Processed {line_count} lines.')



print("Done")

