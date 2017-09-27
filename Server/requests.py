from __future__ import unicode_literals
import json
import datetime
from django.http import JsonResponse, HttpResponse
from bson import BSON, json_util

from database import *
from fetch import fetchData
from logs import saveLog

def responseTest(data):
    client = connectMongoDB()
    collection = selectCollectionMongoDB(client)

    #Add timestamp before fetching
    data["date"] = datetime.datetime.now()

    #Fetch data for multiple purpose
    fetchData(data)

    result = insertElementMongoDB(collection, data)
    strReturn = 'Successfully inserted, with ID: {0}'.format(result.inserted_id)
    saveLog("request.py",strReturn)

    closeMongoDB(client)

    return strReturn

def returnAllDevices():
    client = connectMongoDB()
    collection = selectCollectionMongoDB(client, DBFETCHNAME)

    result = {}
    result['response'] = True
    #Select latest element
    result["devicesList"] = json_util.dumps(selectLatestNElementsMongoDB(collection, 1))

    closeMongoDB(client)

    return result


def IMEIwithSlug(slug):
    client = connectMongoDB()
    collection = selectCollectionMongoDB(client, DBFETCHNAME)

    result = {}
    result["response"] = True
    # result["IMEIList"] = json_util.dumps(selectIMEIForBrand(collection, Brand))
    result["IMEIList"] = json_util.dumps(selectLatestNElementsMongoDB(collection, 1))

    closeMongoDB(client)

    return result

def postRequest(request):
    data = json.loads(request.body)

    print data

    r = data["js_object"]["r"]
    print "request: "+r

    if r == "InsertDevice":
        response = responseTest(data["js_object"])
    elif r == "WebAppAllDevices":
        response = returnAllDevices()
    elif r == "GetIMEIWithSlug":
        response = IMEIwithSlug(data["js_object"]["s"])

    if response is None:
        response = 'errore'

    print "response: "
    print json.dumps(response)

    return response

def getRequest(request):
    return "GET Request with foo: " + request.GET.get('foo', '') + ' and bar: ' + request.GET.get('bar', '')
