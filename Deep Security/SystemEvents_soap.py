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
sheet1 = wb.add_sheet("Deep Security SE Report", cell_overwrite_ok=True)
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


def SystemEvents(sys_id):
    bufferEvent = client.service.systemEventRetrieve2(eventIdFilter = [{'id': sys_id,'operator':'GREATER_THAN'}],timeFilter = [{'type':'CUSTOM_RANGE','rangeFrom':dateNow, 'rangeTo':datetime.datetime.now()}],hostFilter = [{'type':'ALL_HOSTS'}], includeNonHostEvents = False,sID = sessionId)
    json_string = json.loads(json.dumps(bufferEvent, ensure_ascii=False, default=json_default, indent=4).encode('utf-8'))

    return(json_string)

def sys_Query(json_query, x):
    events = []
    eventIDs = []
    for b in json_query['__values__']['systemEvents']['__values__']['item']:
                sysEventID = "".join([str(c) for c in str(b['__values__']['systemEventID'])])
                eventID = "".join([str(c) for c in str(b['__values__']['eventID'])])
                actionPerformedBy = "".join([str(c) for c in str(b['__values__']['actionPerformedBy'])])
                description = "".join([str(c) for c in str(b['__values__']['description'])])
                event = "".join([str(c) for c in str(b['__values__']['event'])])
                eventOrigin = "".join([str(c) for c in str(b['__values__']['eventOrigin'])])
                managerHostname = "".join([str(c) for c in str(b['__values__']['managerHostname'])])
                target = "".join([str(c) for c in str(b['__values__']['target'])])
                targetID = "".join([str(c) for c in str(b['__values__']['targetID'])])
                targetType = "".join([str(c) for c in str(b['__values__']['targetType'])])
                s_type = "".join([str(c) for c in str(b['__values__']['type'])])
                tags = "".join([str(c) for c in str(b['__values__']['tags'])])
                timeM = "".join([str(c) for c in str(b['__values__']['time']['month'])])
                timeD = "".join([str(c) for c in str(b['__values__']['time']['day'])])
                timeY = "".join([str(c) for c in str(b['__values__']['time']['year'])])
                timeh = "".join([str(c) for c in str(b['__values__']['time']['hour'])])
                timem = "".join([str(c) for c in str(b['__values__']['time']['minute'])])
                time_s = "".join([str(c) for c in str(b['__values__']['time']['second'])])
                time_utc = "".join([str(c) for c in str(b['__values__']['time']['utc'])])
                eventDetails = [int(sysEventID), timeM + "/" + timeD + "/" + timeY + " - " + timeh + ":" + timem + ":" + time_s + " " + time_utc + "+0", s_type, eventID, event, target, targetID, targetType, eventOrigin, actionPerformedBy, managerHostname, description.encode("utf-8"), tags]
                events.append(eventDetails)
                eventIDs.append(int(sysEventID))
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
        sheet1.write(x, 11, str(i[11]))
        sheet1.write(x, 12, i[12])
        x+=1
    print("Last Event ID: " + str(eventIDs[-1]))
    print()
    return eventIDs[-1]


#Main Function
sys_event_ID = 0
x = 0

#Excel creation
print("Exporting to xlsx format...")
sleep(3)
sheet1.write(x, 0, "System Event ID")
sheet1.write(x, 1, "Time")
sheet1.write(x, 2, "Type")
sheet1.write(x, 3, "Event ID")
sheet1.write(x, 4, "Event")
sheet1.write(x, 5, "Target")
sheet1.write(x, 6, "Target ID")
sheet1.write(x, 7, "Target Type")
sheet1.write(x, 8, "Event Origin")
sheet1.write(x, 9, "Action Performed By")
sheet1.write(x, 10, "Manager")
sheet1.write(x, 11, "Description")
sheet1.write(x, 12, "Tags")
x+=1

print("Start of fetch")
buff = SystemEvents(sys_event_ID)
sys_event_ID = sys_Query(buff, x)
print("End of fetch")
sleep(5)

while True:
    print()
    print("Start of fetch")
    buffs = SystemEvents(sys_event_ID)
    try:
        sys_event_ID = sys_Query(buffs, x)
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