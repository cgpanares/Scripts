#!/usr/bin/python
from __future__ import print_function
from time import sleep
import os
import sys

def auto_install():
        print("Just installing required modules")
        print("if they do not already exist")
        os.system(" python -m pip install pygresql ")

        sys.exit("\nRequirements installed.\n")


try:
        from pygresql import pgdb
        import getpass

except ImportError:
    auto_install()




hname = input("Enter resolvable hostname of DB: ")
usern = input("Username: ")
passw = getpass.getpass.now()
datab = input("Database Name: ")

hostname = hname
username = usern
password = passw
database = datab

listID = []

def doInsertDatatoBuffer(conn):
    cur = conn.cursor()
    cur.execute( "SELECT * FROM hosts INNER JOIN antiMalwareHosts ON hosts.hostID = antiMalwareHosts.hostID WHERE antiMalwareHosts.AntiMalwareManualScanState = 3 OR antiMalwareHosts.AntiMalwareScheduledScanState = 3;")
    
    for HostID in cur.fetchall():
        listID.append(HostID)
    
    conn.close()
        

def deleteJobSchedScan(conn):
    cur = conn.cursor()
    
    for iD in listID:
        cur.execute("UPDATE antiMalwareHosts SET AntiMalwareScheduledScanState = 0 WHERE AntiMalwareHostID = " + iD)
    
    conn.close()
    

print("Delete Pending Schedule Scan Jobs")
dbConnect = pgdb.connect(host=hostname, user=username, password=password, database=database)
sleep(1)
doInsertDatatoBuffer(dbConnect)
sleep(3)
deleteJobSchedScan(dbConnect)
sys.exit()