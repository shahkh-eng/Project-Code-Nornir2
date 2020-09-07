#Import statements
from nornir import InitNornir
from nornir.plugins.tasks.networking import netmiko_send_command
from nornir.plugins.tasks.networking import napalm_get
from nornir.plugins.functions.text import print_result
from openpyxl import Workbook

#Initialize Nornir with a configuration file
nr = InitNornir("config.yml")
#Create a new Workbook s wb
wb = Workbook()
# Take Active Worksheet as ws
device_ws = wb.active
# Change the title of active workseet to Device Facts
device_ws.title = "Device Facts"
# Create ws for Interface IP Addresses
interfaces_ws = wb.create_sheet("Interface IP")
# Statically assign headers to Device Facts ws
device_headers = ["Device Name","Vendor","Model","OS","Serial","Up Time",]
# Write headers on the top line of the file
device_ws.append(device_headers)
#Nornir to run napalm getters e.g. facts and interfaces_ip
getter_output = nr.run(task=napalm_get, getters=["facts", "interfaces_ip"])
#Print napalm getters output via print_result function
print_result(getter_output)
#For loop to get interusting values from the output
for host, task_results in getter_output.items():
    #Get the device facts result
    device_output = task_results[0].result
    #From Dictionery get vendor name
    vendor = device_output["facts"]["vendor"]
    #From Dictionery get model
    model = device_output["facts"]["model"]
    # From Dictionery get version
    version = device_output["facts"]["os_version"]
    # From Dictionery get serial
    ser_num = device_output["facts"]["serial_number"]
    # From Dictionery get uptime
    uptime = device_output["facts"]["uptime"]
    # Append results to a line to be saved to the worksheet
    line = [host, vendor, model, str(version), str(ser_num), str(uptime),]
    # Save values to row in worksheet
    device_ws.append(line)
    #From Dictionery get interfaces_ip detail
    interfaces_ip = device_output["interfaces_ip"]
    #Wrinting the Host name as Heading in the Interface IP worksheet
    interfaces_ws.append([host])
    #Statically assign headers to Interface IP ws
    interfaces_headers = ["Interface Name", "Ip Address", ]
    #Write headers on the top line of the file
    interfaces_ws.append(interfaces_headers)
    #For Loop to iterate through the Interface ip Dictionery
    for inte, val in interfaces_ip.items():
        #Iterate further to get the IP address of the relevant interface
        ip_address = val["ipv4"].popitem()[0]
        #Append results to a line2 to be saved to the worksheet
        line2 = [str(inte), str(ip_address),]
        #Save values to row in worksheet
        interfaces_ws.append(line2)
# Save workbook
wb.save(filename="device information.xlsx")
