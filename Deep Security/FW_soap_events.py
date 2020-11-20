from requests import Session
from requests.auth import HTTPBasicAuth
import zeep
from zeep.transports import Transport
import datetime
import urllib3
import json
import pprint
import getpass
from time import sleep
import pyexcel_xls
import pyexcel_xlsx
from xlwt import Workbook
import pyexcel as p
import os


#Initialize API Script / Pre-requirements
print("Welcome to DS API - Generating Reports for Toll Holdings!")
url = input("Enter DSM URL: ")
#key = input("Enter API KEY: ")

print("Credentials for the SOAP call. Use DSM login.")

tenant = input("Tenant Name (if using T0, just press enter to leave it blank): ")
user = input("Username: ")
passw = getpass.getpass()
period = input("Input period to be covered from today's date (in days): ")
inputExcelName = input("Desired Filename: ")

#global variables
wb = Workbook()
sheet1 = wb.add_sheet("Deep Security AMEvent Report", cell_overwrite_ok=True)
username = user
password = passw

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
session = Session()
session.verify = False

session.auth = HTTPBasicAuth(username, password)
transport_with_basic_auth = Transport(session=session)

client = zeep.Client(
    wsdl= url + '/webservice/Manager?WSDL',
    transport=transport_with_basic_auth
)

# client.wsdl.dump()
if tenant != "":
    sessionId = client.service.authenticateTenant(tenant,username,password)
else:
    sessionId = client.service.authenticate(username,password)

dateNow = datetime.datetime.now() - datetime.timedelta(days=int(period))


#Functions
def json_default(value):
    if isinstance(value, datetime.datetime):
        return dict(year=value.year, month=value.month, day=value.day, hour = value.hour, minute = value.minute, second = value.second, microsecond = value.microsecond, utc = value.tzinfo.tzname("UTC"))
    else:
        return value.__dict__


def FWEvents(fw_id):
    bufferEvent = client.service.firewallEventRetrieve2(eventIdFilter = [{'id': fw_id,'operator':'GREATER_THAN'}],timeFilter = [{'type':'CUSTOM_RANGE','rangeFrom':dateNow, 'rangeTo':datetime.datetime.now()}],hostFilter = [{'type':'ALL_HOSTS'}],sID = sessionId)
    bufferEvents = [x.encode('utf-8') for x in bufferEvent]
    json_string = json.loads(json.dumps(bufferEvents, ensure_ascii=False, default=json_default, indent=4).encode('utf-8'))
    
    return(json_string)

def fw_Query(json_query, x):
    events = []
    #eventIDs = []
    for b in json_query['__values__']['firewallEvents']['__values__']['item']:
                fwConfig = "".join([str(c) for c in str(b['__values__'])])
                #eventDetails = [int(amEventID), hostID, timeM + "/" + timeD + "/" + timeY + " - " + timeh + ":" + timem + ":" + time_s + " " + time_utc + "+0", malwareName, infectedFilePath, infectionSource, scanType, summaryScanResult, amConfig, malwareType, startTime, endTime, errorCode, protocol, scanAction1, scanAction2, scanResultAction1, scanResultAction2, spywareItems, quarantineRecordID, tags]
                events.append(amConfig)
                #eventIDs.append(int(amEventID))
    #eventIDs.sort()
    for i in events:
        #sheet1.write(x, 0, i[0])
        print(i)
        print()
    print("Last Event ID: " + str(eventIDs[-1]))
    print()
    return eventIDs[-1]


#Main Function
fw_event_ID = 0
x = 0

#Excel creation
print("Exporting to xlsx format...")
sleep(3)
#sheet1.write(x, 0, "AM Event ID")


print("Start of fetch")
buff = FWEvents(fw_event_ID)
fw_event_ID = fw_Query(buff, x)
print("End of fetch")
sleep(5)

while True:
    print()
    print("Start of fetch")
    buffs = FWEvents(fw_event_ID)
    try:
        fw_event_ID = fw_Query(buffs, x)
        print("End of fetch")
        sleep(5)
    except TypeError:
        print("No more to fetch.")
        break

print("Closing connection...")
sleep(3)
client.service.endSession(sessionId)
print("Connection closed.")
# print(client.service.hostRetrieveAll(sID=sessionId))