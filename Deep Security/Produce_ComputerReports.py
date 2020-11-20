from __future__ import print_function
from time import sleep
import os
import sys, warnings

def auto_install():
        print("Just installing required modules")
        print("if they do not already exist")
        os.system(" pip install xlwt ")
        os.system(" pip install pyexcel ")
        os.system(" pip install pyexcel-xls ")
        os.system(" pip install pyexcel-xlsx ")
        os.system(" pip install pyexcel-xlsxw ")
        os.system(" pip install zeep ")
        os.system(" pip install requests ")
        os.system(" pip install urllib3 ")
        os.system(" pip install json ")
        os.system(" pip install getpass ")

        print("\nRequirements installed.\n")

try:
    import deepsecurity
    from deepsecurity.rest import ApiException
    import deepsecurity as api_c
    import pyexcel_xls
    import pyexcel_xlsx
    from xlwt import Workbook
    import pyexcel as p
    import datetime
    import zeep
    from zeep.transports import Transport
    from requests import Session
    from requests.auth import HTTPBasicAuth
    import urllib3
    import json
    import getpass

except:
    auto_install()

print("Welcome to DS API - Generating Reports")
url = input("Enter DSM URL: ")
key = input("Enter API KEY: ")

print("Credentials for the SOAP call. Use DSM login.")

tenant = input("Tenant Name (if using T0, just press enter to leave it blank): ")
user = input("Username: ")
passw = getpass.getpass()
inputExcelName = input("Desired Filename: ")

API_LINK = url + "api"
API_KEY = key

#SOAP Login
username = user
password = passw


####global variables
total_computers_list = []
wb = Workbook()
sheet1 = wb.add_sheet("Deep Security Agent Report", cell_overwrite_ok=True)


# DSAAS API Setup
if not sys.warnoptions:
    warnings.simplefilter("ignore")
configuration = deepsecurity.Configuration()
configuration.host = API_LINK

# Authentication
configuration.api_key['api-secret-key'] = API_KEY

#SOAP authentication
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
session = Session()
session.verify = False

session.auth = HTTPBasicAuth(username, password)
transport_with_basic_auth = Transport(session=session)


# Initialization

#DSAAS SOAP API Setup
client = zeep.Client(
    wsdl= url + '/webservice/Manager?WSDL',
    transport=transport_with_basic_auth
)

# client.wsdl.dump()

if tenant != "":
    sessionId = client.service.authenticateTenant(tenant,username,password)
else:
    sessionId = client.service.authenticate(username,password)

# Set Any Required Values
api_instance1 = deepsecurity.ComputersApi(deepsecurity.ApiClient(configuration))
api_instance2 = deepsecurity.AntiMalwareConfigurationsApi(deepsecurity.ApiClient(configuration))
api_version = 'v1'
overrides = False

dateNow = datetime.datetime.now() - datetime.timedelta(days=15)

def json_default(value):
    if isinstance(value, datetime.datetime):
        return dict(year=value.year, month=value.month, day=value.day, hour = value.hour, minute = value.minute, second = value.second, microsecond = value.microsecond, utc = value.tzinfo.tzname("UTC"))
    else:
        return value.__dict__

#Definition
def ListComputer(ComputerInventory, ruleIDcall, conf, api_v, CompAMInventory):
    bufferEvent = client.service.systemEventRetrieve2(eventIdFilter = [{'id':'0','operator':'GREATER_THAN'}],timeFilter = [{'type':'CUSTOM_RANGE','rangeFrom':dateNow, 'rangeTo':datetime.datetime.now()}],hostFilter = [{'type':'ALL_HOSTS'}],includeNonHostEvents = 'True',sID = sessionId)
    json_string = json.loads(json.dumps(bufferEvent, ensure_ascii=False, default=json_default, indent=4).encode('utf-8'))
    #RecoScan = ruleIDcall.ComputerIntrusionPreventionRuleAssignmentsRecommendationsApi(ruleIDcall.ApiClient(conf))
    x = 0
    print("List All Computers")
    sleep(1)
    print("Exporting to xlsx format...")
    sleep(3)
    sheet1.write(x, 0, "Computer/Host ID")
    sheet1.write(x, 1, "Hostname")
    sheet1.write(x, 2, "Platform")
    sheet1.write(x, 3, "Agent Version")
    sheet1.write(x, 4, "Status")
    sheet1.write(x, 5, "Policy ID")
    sheet1.write(x, 6, "Anti-Malware State")
    sheet1.write(x, 7, "Behavior Monitoring Enabled")
    sheet1.write(x, 8, "Predictive Machine Learning Enabled")
    sheet1.write(x, 9, "IPS state")
    sheet1.write(x, 10, "IM state")
    sheet1.write(x, 11, "LI state")
    sheet1.write(x, 12, "Anti-Malware Last Manual Scan")
    sheet1.write(x, 13, "Completed Malware Scan")
    sheet1.write(x, 14, "Smart Scan Agent Pattern")
    sheet1.write(x, 15, "Virus Pattern (Conventional)")
    sheet1.write(x, 16, "Security Update Status")
    #sheet1.write(x, 17, "Last Recommendation Scan")
    sheet1.write(x, 17, "Self-Protect Enabled")
    sheet1.write(x, 18, "Self-Protect w/ Password Enabled")
    x+=1
    for computer in ComputerInventory.computers:
            comprtID = computer.anti_malware.real_time_scan_configuration_id
            sheet1.write(x, 0, computer.id)
            sheet1.write(x, 1, computer.host_name)
            sheet1.write(x, 2, computer.platform)
            sheet1.write(x, 3, computer.agent_version)
            sheet1.write(x, 4, str(computer.computer_status.agent_status_messages))
            sheet1.write(x, 5, str(computer.policy_id))
            sheet1.write(x, 6, str(computer.anti_malware.module_status.agent_status_message))
            try:
                rtAMid = CompAMInventory.describe_anti_malware(comprtID, api_v)
                if rtAMid:
                    sheet1.write(x, 7, str(rtAMid.behavior_monitoring_enabled))
                    sheet1.write(x, 8, str(rtAMid.machine_learning_enabled))
                else:
                    sheet1.write(x, 7, "No configuration found.")
                    sheet1.write(x, 8, "No configuration found.")
            except:
                sheet1.write(x, 7, "Not Applicable")
                sheet1.write(x, 8, "Not Applicable")
            sheet1.write(x, 9, str(computer.intrusion_prevention.module_status.agent_status_message))
            sheet1.write(x, 10, str(computer.integrity_monitoring.module_status.agent_status_message))
            sheet1.write(x, 11, str(computer.log_inspection.module_status.agent_status_message))
            if str(computer.anti_malware.last_manual_scan) != "None":
                rawtime = str(computer.anti_malware.last_manual_scan)
                splitrt = rawtime[:-3]
                sheet1.write(x, 12, datetime.datetime.fromtimestamp(int(splitrt)).strftime('%Y-%m-%d %H:%M:%S'))
            else:
                sheet1.write(x, 12, str(computer.anti_malware.last_manual_scan))
                
            try:   
                eventList = []
                hostID = str(computer.id)
                for b in json_string['__values__']['systemEvents']['__values__']['item']:
                        if str(b['__values__']['targetID']) == hostID:
                            eventValue = "".join([str(c) for c in str(b['__values__']['eventID'])])
                            timeM = "".join([str(c) for c in str(b['__values__']['time']['month'])])
                            timeD = "".join([str(c) for c in str(b['__values__']['time']['day'])])
                            timeY = "".join([str(c) for c in str(b['__values__']['time']['year'])])
                            timeh = "".join([str(c) for c in str(b['__values__']['time']['hour'])])
                            timem = "".join([str(c) for c in str(b['__values__']['time']['minute'])])
                            time_s = "".join([str(c) for c in str(b['__values__']['time']['second'])])
                            time_utc = "".join([str(c) for c in str(b['__values__']['time']['utc'])])
                            eventwDate = "Event ID: " + eventValue + " -> " + timeM + "/" + timeD + "/" + timeY + " - " + timeh + ":" + timem + ":" + time_s + " " + time_utc + "+0"
                            eventList.append(eventwDate)
                
                for i in eventList:
                    if i.__contains__("Event ID: 1522"):
                        outp = "Done. " + i.replace("Event ID: 1522 ->", "")
                        sheet1.write(x, 13, outp)
                    else:
                        sheet1.write(x, 13, "None")
            except:
                sheet1.write(x, 13, "Not Applicable")
            
            try:
                for su in computer.security_updates.anti_malware:
                    if "Smart Scan Agent Pattern" in str(su.name):
                        sheet1.write(x, 14, str(su.version))
                        sheet1.write(x, 15, "Not Applicable")
                    elif "Virus Pattern" in str(su.name):
                        sheet1.write(x, 14, "Not Applicable")
                        sheet1.write(x, 15, str(su.version))
            except:
                sheet1.write(x, 14, "No Pattern Update")
                sheet1.write(x, 15, "No Pattern Update")
            try:
                sheet1.write(x, 16, str(computer.security_updates.update_status.status_message))
            except:
                sheet1.write(x, 16, "No Security Update Status")
            #try:
                #getRecoScan = RecoScan.list_intrusion_prevention_rule_ids_on_computer(computer.id, api_v, overrides=False)
            #except:
                #getRecoScan = "None"
            #if getRecoScan != "None":
                #if str(getRecoScan.recommendation_scan_status) != "None":
                    #rawtime2 = str(getRecoScan.last_recommendation_scan_date)
                    #splitrt2 = rawtime2[:-3]
                    #try:
                        #sheet1.write(x, 17, datetime.datetime.fromtimestamp(int(splitrt2)).strftime('%Y-%m-%d %H:%M:%S'))
                    #except:
                        #sheet1.write(x, 17, str(getRecoScan.last_recommendation_scan_date))
            #else:
                #sheet1.write(x, 17, "Not Applicable")
            sheet1.write(x, 17, str(computer.computer_settings.platform_setting_agent_self_protection_enabled.value))
            sheet1.write(x, 18, str(computer.computer_settings.platform_setting_agent_self_protection_password_enabled.value))
            x+=1
    wb.save('example.xls')
    fullpath = inputExcelName + ".xlsx"
    p.save_book_as(file_name='example.xls', dest_file_name=fullpath)
    print("Name: " + fullpath)
    print("Saved to same folder of the script!")
    os.remove("example.xls")


#Main Function
print("Importing computers...")
## You can add your code or functions here
try:
                total_computers_list = api_instance1.list_computers(api_version, overrides=overrides)
                totalcomps=len(total_computers_list.computers)
                print(str(totalcomps)+" computers imported into buffer")
                print("Starting...")
                        
except ApiException as e:
                print("An exception occurred: %s\n" % e)
            
if total_computers_list:
                ListComputer(total_computers_list, api_c, configuration, api_version, api_instance2)
                total_computers_list = []
                print("Done!")
                client.service.endSession(sessionId)
                sys.exit()
else:
                sleep(3)
                print("No computers found.")
                client.service.endSession(sessionId)
                sys.exit()