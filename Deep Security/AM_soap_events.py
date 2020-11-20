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


def AMEvents(am_id):
    bufferEvent = client.service.antiMalwareEventRetrieve2(eventIdFilter = [{'id': am_id,'operator':'GREATER_THAN'}],timeFilter = [{'type':'CUSTOM_RANGE','rangeFrom':dateNow, 'rangeTo':datetime.datetime.now()}],hostFilter = [{'type':'ALL_HOSTS'}],sID = sessionId)
    json_string = json.loads(json.dumps(bufferEvent, ensure_ascii=False, default=json_default, indent=4).encode('utf-8'))

    return(json_string)

def am_Query(json_query, x):
    events = []
    eventIDs = []
    for b in json_query['__values__']['antiMalwareEvents']['__values__']['item']:
                amConfig = "".join([str(c) for c in str(b['__values__']['antiMalwareConfigID'])])
                amEventID = "".join([str(c) for c in str(b['__values__']['antiMalwareEventID'])])
                endTime = "".join([str(c) for c in str(b['__values__']['endTime'])])
                errorCode = "".join([str(c) for c in str(b['__values__']['errorCode'])])
                hostID = "".join([str(c) for c in str(b['__values__']['endTime'])])
                infectedFilePath = "".join([str(c) for c in str(b['__values__']['infectedFilePath'])])
                infectionSource = "".join([str(c) for c in str(b['__values__']['infectionSource'])])
                malwareName = "".join([str(c) for c in str(b['__values__']['malwareName'])])
                malwareType = "".join([str(c) for c in str(b['__values__']['malwareType'])])
                protocol = "".join([str(c) for c in str(b['__values__']['protocol'])])
                quarantineRecordID = "".join([str(c) for c in str(b['__values__']['quarantineRecordID'])])
                scanResultAction1 = "".join([str(c) for c in str(b['__values__']['scanResultAction1'])])
                scanResultAction2 = "".join([str(c) for c in str(b['__values__']['scanResultAction2'])])
                scanType = "".join([str(c) for c in str(b['__values__']['scanType'])])
                spywareItems = "".join([str(c) for c in str(b['__values__']['spywareItems']['__values__']['item'])])
                startTime = "".join([str(c) for c in str(b['__values__']['startTime'])])
                tags = "".join([str(c) for c in str(b['__values__']['tags'])])
                scanAction1 = "".join([str(c) for c in str(b['__values__']['scanAction1'])])
                scanAction2 = "".join([str(c) for c in str(b['__values__']['scanAction2'])])
                summaryScanResult = "".join([str(c) for c in str(b['__values__']['summaryScanResult'])])
                timeM = "".join([str(c) for c in str(b['__values__']['logDate']['month'])])
                timeD = "".join([str(c) for c in str(b['__values__']['logDate']['day'])])
                timeY = "".join([str(c) for c in str(b['__values__']['logDate']['year'])])
                timeh = "".join([str(c) for c in str(b['__values__']['logDate']['hour'])])
                timem = "".join([str(c) for c in str(b['__values__']['logDate']['minute'])])
                time_s = "".join([str(c) for c in str(b['__values__']['logDate']['second'])])
                time_utc = "".join([str(c) for c in str(b['__values__']['logDate']['utc'])])
                eventDetails = [int(amEventID), hostID, timeM + "/" + timeD + "/" + timeY + " - " + timeh + ":" + timem + ":" + time_s + " " + time_utc + "+0", malwareName, infectedFilePath, infectionSource, scanType, summaryScanResult, amConfig, malwareType, startTime, endTime, errorCode, protocol, scanAction1, scanAction2, scanResultAction1, scanResultAction2, spywareItems, quarantineRecordID, tags]
                events.append(eventDetails)
                eventIDs.append(int(amEventID))
    eventIDs.sort()
    for i in events:
        sheet1.write(x, 0, i[0])
        sheet1.write(x, 1, i[1])
        sheet1.write(x, 2, i[2])
        sheet1.write(x, 3, i[3])
        sheet1.write(x, 4, i[4])
        sheet1.write(x, 5, i[5])
        sheet1.write(x, 6, i[6])
        sheet1.write(x, 7, i[7])
        sheet1.write(x, 8, i[8])
        sheet1.write(x, 9, i[9])
        sheet1.write(x, 10, i[10])
        sheet1.write(x, 11, i[11])
        sheet1.write(x, 12, i[12])
        sheet1.write(x, 13, i[13])
        sheet1.write(x, 14, i[14])
        sheet1.write(x, 15, i[15])
        sheet1.write(x, 16, i[16])
        sheet1.write(x, 17, i[17])
        sheet1.write(x, 18, i[18])
        sheet1.write(x, 19, i[19])
        sheet1.write(x, 20, i[20])
        x+=1
    print("Last Event ID: " + str(eventIDs[-1]))
    print()
    return eventIDs[-1]


#Main Function
am_event_ID = 0
x = 0

#Excel creation
print("Exporting to xlsx format...")
sleep(3)
sheet1.write(x, 0, "AM Event ID")
sheet1.write(x, 1, "Host ID")
sheet1.write(x, 2, "Time")
sheet1.write(x, 3, "Malware Name")
sheet1.write(x, 4, "Infected File Path")
sheet1.write(x, 5, "Infection Source")
sheet1.write(x, 6, "Scan Type")
sheet1.write(x, 7, "Summary of Scan Result")
sheet1.write(x, 8, "AM Configuration ID")
sheet1.write(x, 9, "Malware Type")
sheet1.write(x, 10, "Start Time")
sheet1.write(x, 11, "End Time")
sheet1.write(x, 12, "Error Code")
sheet1.write(x, 13, "Protocol")
sheet1.write(x, 14, "Scan Action 1")
sheet1.write(x, 15, "Scan Action 2")
sheet1.write(x, 16, "Scan Result Action 1")
sheet1.write(x, 17, "Scan Result Action 2")
sheet1.write(x, 18, "Spyware Items")
sheet1.write(x, 19, "Quarantine Record ID")
sheet1.write(x, 20, "Tags")
x+=1

print("Start of fetch")
buff = AMEvents(am_event_ID)
am_event_ID = am_Query(buff, x)
print("End of fetch")
sleep(5)

while True:
    print()
    print("Start of fetch")
    buffs = AMEvents(am_event_ID)
    try:
        am_event_ID = am_Query(buffs, x)
        print("End of fetch")
        sleep(5)
    except TypeError:
        print("No more to fetch.")
        break

print("Saving excel file...")
wb.save('example.xls')
fullpath = inputExcelName + ".xlsx"
p.save_book_as(file_name='example.xls', dest_file_name=fullpath)
print("Name: " + fullpath)
print("Saved to same folder of the script!")
os.remove("example.xls")

print("Closing connection...")
sleep(3)
client.service.endSession(sessionId)
print("Connection closed.")
# print(client.service.hostRetrieveAll(sID=sessionId))