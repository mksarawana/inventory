#!/usr/bin/python

from __future__ import unicode_literals
from __future__ import print_function
import telnetlib
import sys
import os
import platform
import datetime
import glob
import re
import paramiko
import getpass
import time
import ipaddress
import xlrd
import xlwt


filee = sys.argv[1]
username = sys.argv[2]

################################## Write excel #######################################
new_folder_name = "/var/www/html/test_tart/failovertests/uploads/"+username
if not os.path.exists(new_folder_name):
        os.mkdir(new_folder_name)
        fp = os.path.join(new_folder_name) +"/log.txt"
        with open(fp, "a") as file:
                file.write("\n")
                file.close()
workbook = xlwt.Workbook()
worksheet = workbook.add_sheet('Result', cell_overwrite_ok=True)
print(worksheet)
style1 = xlwt.easyxf('alignment: horiz centre; font: bold on , height 220 ')# for header
style2 = xlwt.easyxf('alignment: horiz centre; font: height 220 ')# for router output entries



#***************** creating header **************************

worksheet.write(0, 0, 'Loopback IP',style1)
worksheet.write(0, 1, 'VRF Name',style1)
worksheet.write(0, 2, 'output',style1)
workbook.save(new_folder_name+'/Result.xls')

###################### core login ###############################

username = ''
pswd = ''
ssh=paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect("100.80.255.217", port=22, username=username,password=pswd,look_for_keys=False, allow_agent=False)
remote_conn = ssh.invoke_shell()
remote_conn.recv(65535)
remote_conn.send(" term len 0 \n")
remote_conn.send(" sh ip bgp vpnv4 vrf volvotucson nei 63.145.144.9 received-routes | in /32 \n")
remote_conn.recv(65535)
time.sleep(.5)
output = remote_conn.recv(65535)
print(output)

print('var/www/html/test_tart/failovertests/'+filee)
file_path = os.path.join(new_folder_name+'/',filee)
print("file path",file_path)
book = xlrd.open_workbook(file_path,"r")
#book = with open(file_path,"rb") as xlsfile
first_sheet = book.sheet_by_index(0)
row_count=first_sheet.nrows
cell_val = first_sheet.cell(1,0)
cell_val_str = str(cell_val).replace(":u","").replace("'","").replace("text","")
print("wswhs",cell_val_str ,type(cell_val_str ),len(cell_val_str ))
for j in range(1,row_count):
        print(j)
	vrf_name = str(first_sheet.cell(j,0)).replace(":u","").replace("'","").replace("text","")
	nei_ip = str(first_sheet.cell(j,1)).replace(":u","").replace("'","").replace("text","")		
	remote_conn.send(" sh ip bgp vpnv4 vrf "+vrf_name+ " nei "+nei_ip+" received-routes | in /32 \n")
	remote_conn.recv(65535)
	time.sleep(.5)
	output = remote_conn.recv(65535)
	print(output,type(output),len(output))
	worksheet.write(j, 0, vrf_name,style2)
	worksheet.write(j, 1, nei_ip,style2)
        worksheet.write(j, 2, output,style2)
        workbook.save(new_folder_name+'/Result.xls')
	print("saves")




download_path = new_folder_name.replace("uploads","logs")
dir = new_folder_name.replace("/var/www/html/test_tart/failovertests/uploads/","")
dir_name = dir+"/"
zip = "cd /var/www/html/test_tart/failovertests/uploads/; tar -zcvf %s.tar.gz %s; cp %s.tar.gz /var/www/html/test_tart/failovertests/logs/ > /dev/null" %(dir,dir_name,dir)
os.system(zip)
#dir_name = '/var/www/html/test_tart/failovertests'
#zip = "cd /var/www/html/test_tart/failovertests/; tar -zcvf %s.tar.gz %s; cp %s.tar.gz /var/www/html/failovertests/logs/ 2> /dev/null" %(dir,dir_name,dir)
#os.system(zip)
#print("File saved path : ",file_save_path)

print("File saved path : ",download_path+".tar.gz")
