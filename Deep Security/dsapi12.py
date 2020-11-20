from __future__ import print_function
from time import sleep
import os
import sys

from Functions.ListComputer import ListComputer
from Functions.SearchComputer import SearchComputer
from Functions.DeleteComputer import DeleteComputer
from Functions.RestartComputer import RestartComputer
from Functions.ModifyComputer import ModifyComputer
from pdb import Restart


def auto_install():
        print("Just installing required modules")
        print("if they do not already exist")
        os.system(" pip install xlwt ")
        os.system(" pip install pyexcel ")
        os.system(" pip install pyexcel-xls ")
        os.system(" pip install pyexcel-xlsx ")
        os.system(" pip install pyexcel-xlsxw ")
        os.system(" pip install pandas ")

        sys.exit("\nRequirements installed.\n")


try:
        import sys, warnings
        import deepsecurity
        from deepsecurity.rest import ApiException
        from xlwt import Workbook
        import pyexcel as p
        import pandas as pd
        import deepsecurity as api_c

except ImportError:
    auto_install()

key = input("Enter API KEY: ")
    
    
API_LINK = 'https://ec2-3-16-252-7.us-east-2.compute.amazonaws.com/api'
API_KEY = key

#MENU SETUP
def print_menu():       ## Your menu design here
    print("----DSaaS Computer Calls----")
    print("1 - Query computers with status equal to ''Reboot''")
    print("2 - Search a Computer")
    print("3 - List All Computers")
    print("4 - Create a Computer")
    print("5 - Delete a Computer")
    print("6 - Modify a Computer")
    print("7 - Close API")
    print("----------------------------")
  
loop=True      
choice=0
########MENU END

####global variables
total_computers_list = []



# DSAAS API Setup
if not sys.warnoptions:
    warnings.simplefilter("ignore")
configuration = deepsecurity.Configuration()
configuration.host = API_LINK

# Authentication
configuration.api_key['api-secret-key'] = API_KEY

# Initialization
# Set Any Required Values
api_instance1 = deepsecurity.ComputersApi(deepsecurity.ApiClient(configuration))
api_version = 'v1'
overrides = False


while loop:          ## While loop which will keep going until loop = False
    print_menu()    ## Displays menu
    ###get controlled input
    test = input("Enter your choice [1-7]: ")
    try:
        choice = int(test)
    except ValueError:
        print("please enter a number instead")
        sleep(3)
        print()


    if choice == 1:
        print("Importing computers...")
        ## You can add your code or functions here
        try:
            
            total_computers_list = api_instance1.list_computers(api_version, overrides=overrides)
            totalcomps=len(total_computers_list.computers)
            print(str(totalcomps)+" computers imported into buffer")
            print("Done!")
            print()
                    
        except ApiException as e:
            print("An exception occurred: %s\n" % e)
        
        if total_computers_list:
            RestartComputer(total_computers_list)
            total_computers_list = []
        else:
            sleep(3)
            print("No computers imported, import computers from DSaaS first!")
            print()
            
    elif choice == 2:
        print("Importing computers...")
        ## You can add your code or functions here
        try:
            
            total_computers_list = api_instance1.list_computers(api_version, overrides=overrides)
            totalcomps=len(total_computers_list.computers)
            print(str(totalcomps)+" computers imported into buffer")
            print("Done!")
            print()
                    
        except ApiException as e:
            print("An exception occurred: %s\n" % e)
        
        if total_computers_list:
            SearchComputer(total_computers_list)
            total_computers_list = []
        else:
            sleep(3)
            print("No computers imported, import computers from DSaaS first!")
            print()    
            
    elif choice == 3:
        print("Importing computers...")
        ## You can add your code or functions here
        try:
            
            total_computers_list = api_instance1.list_computers(api_version, overrides=overrides)
            totalcomps=len(total_computers_list.computers)
            print(str(totalcomps)+" computers imported into buffer")
            print("Done!")
            print()
                    
        except ApiException as e:
            print("An exception occurred: %s\n" % e)
        
        if total_computers_list:
            ListComputer(total_computers_list)
            total_computers_list = []
        else:
            sleep(3)
            print("No computers imported, import computers from DSaaS first!")
            print()
            
    elif choice==4:
        print("Importing computers...")
        ## You can add your code or functions here
        try:
            
            total_computers_list = api_instance1.list_computers(api_version, overrides=overrides)
            totalcomps=len(total_computers_list.computers)
            print(str(totalcomps)+" computers imported into buffer")
            print("Done!")
            print()
                    
        except ApiException as e:
            print("An exception occurred: %s\n" % e)
            
        if total_computers_list:
            print("Menu 5 - Create a Computer")
            print("Function not done yet.")
            print("Done!")
            print()
        else:
            sleep(3)
            print("No computers imported, import computers from DSaaS first!")
            print()
            
    elif choice==5:
        print("Importing computers...")
        ## You can add your code or functions here
        try:
            
            total_computers_list = api_instance1.list_computers(api_version, overrides=overrides)
            totalcomps=len(total_computers_list.computers)
            print(str(totalcomps)+" computers imported into buffer")
            print("Done!")
            print()
                    
        except ApiException as e:
            print("An exception occurred: %s\n" % e)
            
        if total_computers_list:
            DeleteComputer(api_instance1, api_version, total_computers_list)
            total_computers_list = []
        else:
            sleep(3)
            print("No computers imported, import computers from DSaaS first!")
            print()
            
    elif choice==6:
        print("Importing computers...")
        ## You can add your code or functions here
        try:
            
            total_computers_list = api_instance1.list_computers(api_version, overrides=overrides)
            totalcomps=len(total_computers_list.computers)
            print(str(totalcomps)+" computers imported into buffer")
            print("Done!")
            print()
                    
        except ApiException as e:
            print("An exception occurred: %s\n" % e)
            
        if total_computers_list:
            ModifyComputer(api_instance1, api_version, total_computers_list, api_c)
            total_computers_list = []
        else:
            sleep(3)
            print("No computers imported, import computers from DSaaS first!")
            print()
            
    elif choice==7:
        print("Closing...")
        sleep(3)
        print("Successfully closed.")
        loop=False # This will make the while loop to end as not value of loop is set to False but it did not work under python3 so I used break instead.
        break
    else:
        # Any integer inputs other than values 1-5 we print an error message
        print("Wrong option selection. Enter any key to try again..")