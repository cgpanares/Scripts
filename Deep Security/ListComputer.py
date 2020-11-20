import sys
import os
import time
from time import sleep
from xlwt import Workbook
import pyexcel as p
import datetime


wb = Workbook()
sheet1 = wb.add_sheet("Deep Security Agent Report", cell_overwrite_ok=True)



def printMenu():
    print("Based on Status")
    print("1 - Online")
    print("2 - Offline")
    print("3 - Others")
    print("4 - All")


def ListComputer(ComputerInventory):
    x = 0
    print("Menu 3 - List All Computers")
    printMenu()
    inputChoice = input("Enter choice: ")
    sleep(3)
    if inputChoice == "1":
        for computer in ComputerInventory.computers:
            if "Online" in str(computer.computer_status.agent_status_messages):
                print("Hostname: " + computer.host_name)
                print("Platform: " + computer.platform)
                print("Relay State" + computer.computer_settings.platform_setting_relay_state.value)
                print("Agent Version: " + computer.agent_version)
                print("Status: " + str(computer.computer_status.agent_status_messages))
                print("Anti-Malware State: " + str(computer.anti_malware.module_status.agent_status_message))
                if str(computer.anti_malware.last_manual_scan) != "None":
                    rawtime = str(computer.anti_malware.last_manual_scan)
                    splitrt = rawtime[:-3]
                    print("Anti-Malware Last Manual Scan: " + datetime.datetime.fromtimestamp(int(splitrt)).strftime('%Y-%m-%d %H:%M:%S'))
                else:
                    print("Anti-Malware Last Manual Scan: " + str(computer.anti_malware.last_manual_scan))
                if str(computer.anti_malware.last_scheduled_scan) != "None":
                    rawtime = str(computer.anti_malware.last_scheduled_scan)
                    splitrt = rawtime[:-3]
                    print("Anti-Malware Last Manual Scan: " + datetime.datetime.fromtimestamp(int(splitrt)).strftime('%Y-%m-%d %H:%M:%S'))
                else:
                    print("Anti-Malware Last Manual Scan: " + str(computer.anti_malware.last_scheduled_scan))
                for su in computer.security_updates.anti_malware:
                    print("Name: " + str(su.name) + " Version: " + str(su.version) + " is this latest?: " + str(su.latest))
                print("#-------------------------------------------------#")
            else:
                ListComputer(ComputerInventory)
        inputExcel = input("Do you want to export the results in an excel file?(y/n): ")
        if "y" in inputExcel:
                inputExcelName = input("Desired Filename: ")
                print("Exporting to excel (.xlsx)...")
                sleep(3)
                totalC = len(ComputerInventory.computers)
                sheet1.write(x, 0, "Total Number of Machines: ")
                sheet1.write(x, 1, str(totalC))
                x+=1
                sheet1.write(x, 0, "")
                sheet1.write(x, 1, "")
                x+=1
                for computer in ComputerInventory.computers:
                    if "Online" in str(computer.computer_status.agent_status_messages):
                        sheet1.write(x, 0, "Hostname: ")
                        sheet1.write(x, 1, computer.host_name)
                        x+=1
                        sheet1.write(x, 0, "Platform: ")
                        sheet1.write(x, 1, computer.platform)
                        x+=1
                        sheet1.write(x, 0, "Agent Version: ")
                        sheet1.write(x, 1, computer.agent_version)
                        x+=1
                        sheet1.write(x, 0, "Status: ")
                        sheet1.write(x, 1, str(computer.computer_status.agent_status_messages))
                        x+=1
                        sheet1.write(x, 0, "Anti-Malware State: ")
                        sheet1.write(x, 1, str(computer.anti_malware.module_status.agent_status_message))
                        x+=1
                        if str(computer.anti_malware.last_manual_scan) != "None":
                            rawtime = str(computer.anti_malware.last_manual_scan)
                            splitrt = rawtime[:-3]
                            sheet1.write(x, 0, "Anti-Malware Last Manual Scan: ")
                            sheet1.write(x, 1, datetime.datetime.fromtimestamp(int(splitrt)).strftime('%Y-%m-%d %H:%M:%S'))
                            x+=1
                        else:
                            sheet1.write(x, 0, "Anti-Malware Last Manual Scan: ")
                            sheet1.write(x, 1, str(computer.anti_malware.last_manual_scan))
                            x+=1
                        if str(computer.anti_malware.last_scheduled_scan) != "None":
                            rawtime = str(computer.anti_malware.last_scheduled_scan)
                            splitrt = rawtime[:-3]
                            sheet1.write(x, 0, "Anti-Malware Last Scheduled Scan: ")
                            sheet1.write(x, 1, datetime.datetime.fromtimestamp(int(splitrt)).strftime('%Y-%m-%d %H:%M:%S'))
                            x+=1
                        else:
                            sheet1.write(x, 0, "Anti-Malware Last Scheduled Scan: ")
                            sheet1.write(x, 1, str(computer.anti_malware.last_scheduled_scan))
                            x+=1
                        for su in computer.security_updates.anti_malware:
                            sheet1.write(x, 0, "Name, Version, Latest?: ")
                            sheet1.write(x, 1, str(su.name) + ", " + str(su.version)  + ", " + str(su.latest))
                            x+=1
                        sheet1.write(x, 1, "")
                        x+=1
                wb.save('example.xls')
                fullpath = inputExcelName + ".xlsx"
                p.save_book_as(file_name='example.xls', dest_file_name=fullpath)
                print("Name: " + fullpath)
                print("Saved to same folder of the script!")
                os.remove("example.xls")
        else:
                print("Exporting to excel did not proceed.")
                print("Done!")
                print()
    elif inputChoice == "2":
        for computer in ComputerInventory.computers:
            if "Offline" in str(computer.computer_status.agent_status_messages):
                print("Hostname: " + computer.host_name)
                print("Platform: " + computer.platform)
                print("Agent Version: " + computer.agent_version)
                print("Status: " + str(computer.computer_status.agent_status_messages))
                print("Anti-Malware State: " + str(computer.anti_malware.module_status.agent_status_message))
                if str(computer.anti_malware.last_manual_scan) != "None":
                    rawtime = str(computer.anti_malware.last_manual_scan)
                    splitrt = rawtime[:-3]
                    print("Anti-Malware Last Manual Scan: " + datetime.datetime.fromtimestamp(int(splitrt)).strftime('%Y-%m-%d %H:%M:%S'))
                else:
                    print("Anti-Malware Last Manual Scan: " + str(computer.anti_malware.last_manual_scan))
                if str(computer.anti_malware.last_scheduled_scan) != "None":
                    rawtime = str(computer.anti_malware.last_scheduled_scan)
                    splitrt = rawtime[:-3]
                    print("Anti-Malware Last Manual Scan: " + datetime.datetime.fromtimestamp(int(splitrt)).strftime('%Y-%m-%d %H:%M:%S'))
                else:
                    print("Anti-Malware Last Manual Scan: " + str(computer.anti_malware.last_scheduled_scan))
                for su in computer.security_updates.anti_malware:
                    print("Name: " + str(su.name) + " Version: " + str(su.version) + " is this latest?: " + str(su.latest))
                print("#-------------------------------------------------#")
            else:
                ListComputer(ComputerInventory)
        inputExcel = input("Do you want to export the results in an excel file?(y/n): ")
        if "y" in inputExcel:
                inputExcelName = input("Desired Filename: ")
                print("Exporting to excel (.xlsx)...")
                sleep(3)
                totalC = len(ComputerInventory.computers)
                sheet1.write(x, 0, "Total Number of Machines: ")
                sheet1.write(x, 1, str(totalC))
                x+=1
                sheet1.write(x, 0, "")
                sheet1.write(x, 1, "")
                x+=1
                for computer in ComputerInventory.computers:
                    if "Offline" in str(computer.computer_status.agent_status_messages):
                        sheet1.write(x, 0, "Hostname: ")
                        sheet1.write(x, 1, computer.host_name)
                        x+=1
                        sheet1.write(x, 0, "Platform: ")
                        sheet1.write(x, 1, computer.platform)
                        x+=1
                        sheet1.write(x, 0, "Agent Version: ")
                        sheet1.write(x, 1, computer.agent_version)
                        x+=1
                        sheet1.write(x, 0, "Status: ")
                        sheet1.write(x, 1, str(computer.computer_status.agent_status_messages))
                        x+=1
                        sheet1.write(x, 0, "Anti-Malware State: ")
                        sheet1.write(x, 1, str(computer.anti_malware.module_status.agent_status_message))
                        x+=1
                        if str(computer.anti_malware.last_manual_scan) != "None":
                            rawtime = str(computer.anti_malware.last_manual_scan)
                            splitrt = rawtime[:-3]
                            sheet1.write(x, 0, "Anti-Malware Last Manual Scan: ")
                            sheet1.write(x, 1, datetime.datetime.fromtimestamp(int(splitrt)).strftime('%Y-%m-%d %H:%M:%S'))
                            x+=1
                        else:
                            sheet1.write(x, 0, "Anti-Malware Last Manual Scan: ")
                            sheet1.write(x, 1, str(computer.anti_malware.last_manual_scan))
                            x+=1
                        if str(computer.anti_malware.last_scheduled_scan) != "None":
                            rawtime = str(computer.anti_malware.last_scheduled_scan)
                            splitrt = rawtime[:-3]
                            sheet1.write(x, 0, "Anti-Malware Last Scheduled Scan: ")
                            sheet1.write(x, 1, datetime.datetime.fromtimestamp(int(splitrt)).strftime('%Y-%m-%d %H:%M:%S'))
                            x+=1
                        else:
                            sheet1.write(x, 0, "Anti-Malware Last Scheduled Scan: ")
                            sheet1.write(x, 1, str(computer.anti_malware.last_scheduled_scan))
                            x+=1
                        for su in computer.security_updates.anti_malware:
                            sheet1.write(x, 0, "Name, Version, Latest?: ")
                            sheet1.write(x, 1, str(su.name) + ", " + str(su.version)  + ", " + str(su.latest))
                            x+=1
                        sheet1.write(x, 1, "")
                        x+=1
                wb.save('example.xls')
                fullpath = inputExcelName + ".xlsx"
                p.save_book_as(file_name='example.xls', dest_file_name=fullpath)
                print("Name: " + fullpath)
                print("Saved to same folder of the script!")
                os.remove("example.xls")
        else:
                print("Exporting to excel did not proceed.")
                print("Done!")
                print()
    elif inputChoice == "3":
        for computer in ComputerInventory.computers:
            if "Online" and "Offline" not in str(computer.computer_status.agent_status_messages):
                print("Hostname: " + computer.host_name)
                print("Platform: " + computer.platform)
                print("Agent Version: " + computer.agent_version)
                print(computer.ec2_virtual_machine_summary.metadata[0])
                print("Status: " + str(computer.computer_status.agent_status_messages))
                print("Anti-Malware State: " + str(computer.anti_malware.module_status.agent_status_message))
                if str(computer.anti_malware.last_manual_scan) != "None":
                    rawtime = str(computer.anti_malware.last_manual_scan)
                    splitrt = rawtime[:-3]
                    print("Anti-Malware Last Manual Scan: " + datetime.datetime.fromtimestamp(int(splitrt)).strftime('%Y-%m-%d %H:%M:%S'))
                else:
                    print("Anti-Malware Last Manual Scan: " + str(computer.anti_malware.last_manual_scan))
                if str(computer.anti_malware.last_scheduled_scan) != "None":
                    rawtime = str(computer.anti_malware.last_scheduled_scan)
                    splitrt = rawtime[:-3]
                    print("Anti-Malware Last Manual Scan: " + datetime.datetime.fromtimestamp(int(splitrt)).strftime('%Y-%m-%d %H:%M:%S'))
                else:
                    print("Anti-Malware Last Manual Scan: " + str(computer.anti_malware.last_scheduled_scan))
                for su in computer.security_updates.anti_malware:
                    print("Name: " + str(su.name) + " Version: " + str(su.version) + " is this latest?: " + str(su.latest))
                print("#-------------------------------------------------#")
            else:
                ListComputer(ComputerInventory)
        inputExcel = input("Do you want to export the results in an excel file?(y/n): ")
        if "y" in inputExcel:
                inputExcelName = input("Desired Filename: ")
                print("Exporting to excel (.xlsx)...")
                sleep(3)
                totalC = len(ComputerInventory.computers)
                sheet1.write(x, 0, "Total Number of Machines: ")
                sheet1.write(x, 1, str(totalC))
                x+=1
                sheet1.write(x, 0, "")
                sheet1.write(x, 1, "")
                x+=1
                for computer in ComputerInventory.computers:
                    if "Online" and "Offline" not in str(computer.computer_status.agent_status_messages):
                        sheet1.write(x, 0, "Hostname: ")
                        sheet1.write(x, 1, computer.host_name)
                        x+=1
                        sheet1.write(x, 0, "Platform: ")
                        sheet1.write(x, 1, computer.platform)
                        x+=1
                        sheet1.write(x, 0, "Agent Version: ")
                        sheet1.write(x, 1, computer.agent_version)
                        x+=1
                        sheet1.write(x, 0, "Status: ")
                        sheet1.write(x, 1, str(computer.computer_status.agent_status_messages))
                        x+=1
                        sheet1.write(x, 0, "Anti-Malware State: ")
                        sheet1.write(x, 1, str(computer.anti_malware.module_status.agent_status_message))
                        x+=1
                        if str(computer.anti_malware.last_manual_scan) != "None":
                            rawtime = str(computer.anti_malware.last_manual_scan)
                            splitrt = rawtime[:-3]
                            sheet1.write(x, 0, "Anti-Malware Last Manual Scan: ")
                            sheet1.write(x, 1, datetime.datetime.fromtimestamp(int(splitrt)).strftime('%Y-%m-%d %H:%M:%S'))
                            x+=1
                        else:
                            sheet1.write(x, 0, "Anti-Malware Last Manual Scan: ")
                            sheet1.write(x, 1, str(computer.anti_malware.last_manual_scan))
                            x+=1
                        if str(computer.anti_malware.last_scheduled_scan) != "None":
                            rawtime = str(computer.anti_malware.last_scheduled_scan)
                            splitrt = rawtime[:-3]
                            sheet1.write(x, 0, "Anti-Malware Last Scheduled Scan: ")
                            sheet1.write(x, 1, datetime.datetime.fromtimestamp(int(splitrt)).strftime('%Y-%m-%d %H:%M:%S'))
                            x+=1
                        else:
                            sheet1.write(x, 0, "Anti-Malware Last Scheduled Scan: ")
                            sheet1.write(x, 1, str(computer.anti_malware.last_scheduled_scan))
                            x+=1
                        for su in computer.security_updates.anti_malware:
                            sheet1.write(x, 0, "Name, Version, Latest?: ")
                            sheet1.write(x, 1, str(su.name) + ", " + str(su.version)  + ", " + str(su.latest))
                            x+=1
                        sheet1.write(x, 1, "")
                        x+=1
                wb.save('example.xls')
                fullpath = inputExcelName + ".xlsx"
                p.save_book_as(file_name='example.xls', dest_file_name=fullpath)
                print("Name: " + fullpath)
                print("Saved to same folder of the script!")
                os.remove("example.xls")
        else:
                print("Exporting to excel did not proceed.")
                print("Done!")
                print()
    elif inputChoice == "4":
        for computer in ComputerInventory.computers:
            if(computer.group_id == 1):
                print("Hostname: " + computer.host_name)
                print("Platform: " + computer.platform)
                print("Agent Version: " + computer.agent_version)
                print("Status: " + str(computer.computer_status.agent_status_messages))
                print("Anti-Malware State: " + str(computer.anti_malware.module_status.agent_status_message))
                print("Agent Task: " + str(computer.tasks))
                if str(computer.anti_malware.last_manual_scan) != "None":
                    rawtime = str(computer.anti_malware.last_manual_scan)
                    splitrt = rawtime[:-3]
                    print("Anti-Malware Last Manual Scan: " + datetime.datetime.fromtimestamp(int(splitrt)).strftime('%Y-%m-%d %H:%M:%S'))
                else:
                    print("Anti-Malware Last Manual Scan: " + str(computer.anti_malware.last_manual_scan))
                if str(computer.anti_malware.last_scheduled_scan) != "None":
                    rawtime = str(computer.anti_malware.last_scheduled_scan)
                    splitrt = rawtime[:-3]
                    print("Anti-Malware Last Manual Scan: " + datetime.datetime.fromtimestamp(int(splitrt)).strftime('%Y-%m-%d %H:%M:%S'))
                else:
                    print("Anti-Malware Last Manual Scan: " + str(computer.anti_malware.last_scheduled_scan))
                for su in computer.security_updates.anti_malware:
                    print("Name: " + str(su.name) + " Version: " + str(su.version) + " is this latest?: " + str(su.latest))
                print("#-------------------------------------------------#")
        inputExcel = input("Do you want to export the results in an excel file?(y/n): ")
        if "y" in inputExcel:
                inputExcelName = input("Desired Filename: ")
                print("Exporting to excel (.xlsx)...")
                sleep(3)
                totalC = len(ComputerInventory.computers)
                sheet1.write(x, 0, "Total Number of Machines: ")
                sheet1.write(x, 1, str(totalC))
                x+=1
                sheet1.write(x, 0, "")
                sheet1.write(x, 1, "")
                x+=1
                for computer in ComputerInventory.computers:
                    if(computer.group_id == 1):
                        sheet1.write(x, 0, "Hostname: ")
                        sheet1.write(x, 1, computer.host_name)
                        x+=1
                        sheet1.write(x, 0, "Platform: ")
                        sheet1.write(x, 1, computer.platform)
                        x+=1
                        sheet1.write(x, 0, "Agent Version: ")
                        sheet1.write(x, 1, computer.agent_version)
                        x+=1
                        sheet1.write(x, 0, "Status: ")
                        sheet1.write(x, 1, str(computer.computer_status.agent_status_messages))
                        x+=1
                        sheet1.write(x, 0, "Anti-Malware State: ")
                        sheet1.write(x, 1, str(computer.anti_malware.module_status.agent_status_message))
                        x+=1
                        if str(computer.anti_malware.last_manual_scan) != "None":
                            rawtime = str(computer.anti_malware.last_manual_scan)
                            splitrt = rawtime[:-3]
                            sheet1.write(x, 0, "Anti-Malware Last Manual Scan: ")
                            sheet1.write(x, 1, datetime.datetime.fromtimestamp(int(splitrt)).strftime('%Y-%m-%d %H:%M:%S'))
                            x+=1
                        else:
                            sheet1.write(x, 0, "Anti-Malware Last Manual Scan: ")
                            sheet1.write(x, 1, str(computer.anti_malware.last_manual_scan))
                            x+=1
                        if str(computer.anti_malware.last_scheduled_scan) != "None":
                            rawtime = str(computer.anti_malware.last_scheduled_scan)
                            splitrt = rawtime[:-3]
                            sheet1.write(x, 0, "Anti-Malware Last Scheduled Scan: ")
                            sheet1.write(x, 1, datetime.datetime.fromtimestamp(int(splitrt)).strftime('%Y-%m-%d %H:%M:%S'))
                            x+=1
                        else:
                            sheet1.write(x, 0, "Anti-Malware Last Scheduled Scan: ")
                            sheet1.write(x, 1, str(computer.anti_malware.last_scheduled_scan))
                            x+=1
                        for su in computer.security_updates.anti_malware:
                            sheet1.write(x, 0, "Name, Version, Latest?: ")
                            sheet1.write(x, 1, str(su.name) + ", " + str(su.version)  + ", " + str(su.latest))
                            x+=1
                        sheet1.write(x, 1, "")
                        x+=1
                wb.save('example.xls')
                fullpath = inputExcelName + ".xlsx"
                p.save_book_as(file_name='example.xls', dest_file_name=fullpath)
                print("Name: " + fullpath)
                print("Saved to same folder of the script!")
                os.remove("example.xls")
        else:
                print("Exporting to excel did not proceed.")
                print("Done!")
                print()
    else:
        print("Choose a number that exists in the choices!")