#!/usr/bin/python
from __future__ import print_function
import sys
import telnetlib
import datetime
import os
import csv
import random
import string
import array
import subprocess
import ipaddress
import xlwt
import xlrd
import platform
import time
import re

users_list = []
default_router_password = ''
default_enable_password = ''
remarks = []

username = sys.argv[2]
filee = sys.argv[1]
print(filee)
print(username)
#result_path = '/var/www/html/test_tart/failovertests/logs/'+user

#new_folder_name = "/var/www/html/failovertests/uploads/"+username+"_"+datetime.datetime.now().strftime("%m-%d-%y_%H-%M-%S")
#if not os.path.exists(new_folder_name):
#	os.mkdir(new_folder_name)

############################# Login process ##########################################
def auto_router_login():
        tryy = 0
	#print("auto done")
        for x in users_list:
                r1_bool = False
                time.sleep(1)
                tel_res = tel.read_until("sername: ".encode('ascii'),2)# Regular login attempt
		
		#print(tel_res)
                time.sleep(1)
                tel.write((x + '\r').encode('ascii'))
                tel.read_until('assword: '.encode('ascii'),2)
                tel.write((default_router_password + '\r' + '\n \n').encode('ascii'))
        #       time.sleep(1.2)
                tryy = tryy + 1
                login_status = tel.read_until(">".encode('ascii'),2)
		#print(login_status)
                if bool(re.search(">",login_status.decode("utf-8"))) is True:
#                        print("default login success")
                        r1_bool = True
                        if enab() == True:
                        	break
			else:
				r1_bool = False
                else:
        #               print "Error Credentials on both the attempts.\n"
                        r1_bool = False
        return r1_bool

def enab():
        enab_bool = False
        #print ("Trying Enable login now")
        tel.write("en\r".encode('ascii'))
        #print(tel.read_until('assword: '.encode('ascii'),2))
        tel.read_until('assword: '.encode('ascii'),2)
        tel.write((default_enable_password + '\r').encode('ascii'))
        enab_status = tel.read_until("#".encode('ascii'), 2)
	print(enab_status)
        if bool(re.search("#",enab_status.decode("utf-8"))) is True:
                #print ("Auto ENABLE CREDENTIALS worked!")
                enab_bool = True
		toc()
#		print("status",status)
	
        #elif bool(re.search("assword:",enab_status.decode("utf-8"))) is True:
		#continue
                #print ("AUTO ENABLE CREDENTIALS DID NOT WORK.")
        #       print "\nCustomer might be having CUSTOM PREVILIDGE PASSWORD. Please refer NETLIB or CRYPTO TOOL to know the password. \n Please enter the password below:\n"
                #man_enab_pwd = raw_input('Please enter the CUSTOM ENABLE password here: ')
                #tel.read_until('assword: '.encode('ascii'))
                #tel.write((man_enab_pwd + '\r').encode('ascii'))
                #if tel.read_until("#".encode('ascii'), 2):
        #                       print "Manual ENABLE CREDENTIALS worked! Previlidged access achieved\n\n"
                        #enab_bool = True
		#continue

        else:
                print ("ERROR IN CUSTOM ENABLE PASSWORD")
                enab_bool = False
		#continue
        return enab_bool


def isUp(hostname):
        response = ""
#	print(hostname)
        if platform.system() == "Windows":
         #       print ("Pinging Windows")
                response = os.system("ping "+hostname+"> /dev/null")
 #               print ("\nPing from WINDOWS PC is successful. \nThe client " + hostname + " is LIVE!\n")
        else:
          #      print ("Pinging Linux")
                response = os.system("ping -c 1 "+hostname+" > /dev/null")
   #             print ("\nPing from LINUX PC is successful. \nThe client " + hostname + " is LIVE!\n")
        isUpBool = ""
        if response == 0:
		worksheet.write(j, 2, 'success',style2)
		workbook.save(new_folder_name+'/Result.xls')
                print (hostname, 'is up!')
                isUpBool = True
        else:
		worksheet.write(j, 3, 'failed',style1)
		workbook.save(new_folder_name+'/Result.xls')
            	print (hostname, 'is down!')
	return isUpBool
################################ Type of connectivity ########################################
def toc():
	sdn = []
	remarks[:] = []
	gre = ''
	tunnels = ["Tunnel17127","Tunnel40443"]
	#print("entered to the function")
	tel.write("ter len 0 \r".encode('ascii'))
        tel.read_until("#".encode('ascii'))
	tel.write(('show ip bgp summary ' + '\r').encode('ascii'))
        bgp_result = tel.read_until("#".encode('ascii'))
	tel.write("sh run | sec bgp\r".encode('ascii'))
    	bgp_config = tel.read_until("#".encode('ascii'))
        as_num = re.findall("BGP router identifier (.+?)\n",bgp_result.decode("utf-8"))
        print(as_num)
        for pri_as in range(64512,65536):
        	if bool(re.search(str(pri_as),str(as_num))) is True:
			as_find = re.findall(' remote-as (.+?)\n',bgp_config.decode("utf-8"))
			print("as find",as_find)
			asn = str(as_find).replace("'","").replace("u","").replace("\\r","").replace("[","").replace("]","")
			print("asn",asn)
			worksheet.write(j, 4, 'sdn',style2)
			worksheet.write(j, 9, asn,style2)
			workbook.save(new_folder_name+'/Result.xls')
			fp = os.path.join(new_folder_name) +"/log.txt"
                        with open(fp, "a") as file:
                                file.write("SDN found on "+host_ip+" \n")
                                file.close()
       			print("ITZ SDN")
			sdn.append("True")
	for tun_int in tunnels:
                #print(tun_int)
                tel.write(('show run int '+tun_int + '\r').encode('ascii'))
                tunnel_result = tel.read_until("#".encode('ascii'),2)
		#print(tunnel_result)
                if bool(re.search('ip nat outside',tunnel_result.decode("utf-8"))) is True:
			remarks.append(tun_int)
			worksheet.write(j, 5, 'yes',style2)
			workbook.save(new_folder_name+'/Result.xls')
			fp = os.path.join(new_folder_name) +"/log.txt"
                        with open(fp, "a") as file:
                                file.write("GRE tunnel found on "+host_ip+"\n")
                                file.close()
                        print("Itz GRE Tunnel")
			sdn.append( "False")
		#else:
			#continue
		
		tel.write('show ip eigrp nei\r'.encode('ascii'))
                eigrp_result = tel.read_until("#".encode('ascii'),2)
		#print(eigrp_result)
		#print(tun_int)
		if bool(re.search(tun_int.replace("nnel",""),eigrp_result.decode('utf-8'))) is True:
			worksheet.write(j, 6, 'yes',style2)
			workbook.save(new_folder_name+'/Result.xls')
			fp = os.path.join(new_folder_name) +"/log.txt"
                        with open(fp, "a") as file:
                                file.write("GRE found and its EIGRP on "+host_ip+" \n")
                                file.close()
			print("ITZ eigrp")
			sdn.append("false")
	print("Sdn ",sdn)
	if len(sdn) == 0:
		worksheet.write(j, 7, 'none',style2)
		workbook.save(new_folder_name+'/Result.xls')
		fp = os.path.join(new_folder_name) +"/log.txt"
                with open(fp, "a") as file:
                	file.write("Neither GRE nor SDN "+host_ip+"\n")
                        file.close()
		print("Neither GRE nor SDN found")
	worksheet.write(j, 8, str(remarks).replace("'","").replace("[","").replace("]",""),style2)
	'''
	for tun_int in tunnels:
		#print(tun_int)
		tel.write(('show run int '+tun_int + '\r').encode('ascii'))
		tunnel_result = tel.read_until("#".encode('ascii'))
		if bool(re.search('ip nat outside',tunnel_result.decode("utf-8"))) is True:
			print("Itz GRE")
			sdn = "False"
			#break

		elif bool(re.search('ip nat outside',tunnel_result.decode("utf-8"))) is not True:
			tel.write(('show ip bgp summary ' + '\r').encode('ascii'))
                	bgp_result = tel.read_until("#".encode('ascii'))
			as_num = re.findall("BGP router identifier (.+?)\n",bgp_result.decode("utf-8"))
			print(as_num)
			for pri_as in range(65006,65008):
				if bool(re.search(str(pri_as),str(as_num))) is True:
					print("ITZ SDN")
					break	
					gre = "False"
				else:
					print("Neither GRE nor SDN found")
				#	break
		#print(tunnel_result.decode("utf-8"))
		print("gre status",gre)

'''
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

worksheet.write(0, 0, 'IP Address',style1)
worksheet.write(0, 1, 'Telnet enabled?',style1)
worksheet.write(0, 2, 'Reachability',style1)
worksheet.write(0, 3, 'Authendication',style1)
worksheet.write(0, 4, 'Sdn',style1)
worksheet.write(0, 5, 'Tunnel',style1)
worksheet.write(0, 6, 'Eigrp',style1)
worksheet.write(0, 7, 'None',style1)
worksheet.write(0, 8, 'Remarks',style1)
worksheet.write(0, 9, 'AS',style1)
workbook.save(new_folder_name+'/Result.xls')
################################## read excel #################################

# "/var/www/html/failovertests/uploads/"+username+"_"+datetime.datetime.now().strftime("%m-%d-%y_%H-%M-%S")
#new_folder_name = "/var/www/html/test_tart/failovertests/uploads/"+username
#if not os.path.exists(new_folder_name):
 #       os.mkdir(new_folder_name)
#	fp = os.path.join(new_folder_name) +"/log.txt"
 #       with open(fp, "a") as file:
  #      	file.write("\n")
   #             file.close()


move_input_file = "cd /var/www/html/test_tart/failovertests/uploads; mv "+filee+" "+new_folder_name+"/"
print("ads",move_input_file)
os.system(move_input_file)
zip = "cd  "
new_folder_name

print('var/www/html/test_tart/failovertests/'+filee)
file_path = os.path.join(new_folder_name+'/',filee)
print("file path",file_path)
book = xlrd.open_workbook(file_path,"r")
#book = with open(file_path,"rb") as xlsfile
first_sheet = book.sheet_by_index(0)
row_count=first_sheet.nrows
print(first_sheet)
for j in range(1,row_count):
	print(j)
	
    	list_host=first_sheet.row_values(j)
   	host=str(list_host)
   	host_ip=host.replace("'",'').replace('"','').replace("]",'').replace("[",'').replace("u","").replace(",","")
   	print(host_ip)
	worksheet.write(j, 0, host_ip,style2)
	workbook.save(new_folder_name+'/Result.xls')
	if isUp(host_ip) == True:
		try:
        		tel = telnetlib.Telnet(host_ip)
			worksheet.write(j, 1, 'Enabled',style2)
			workbook.save(new_folder_name+'/Result.xls')
		except:
			worksheet.write(j, 1, 'Not Enabled',style1)
			workbook.save(new_folder_name+'/Result.xls')
			print("please enable telnet")
			continue
		
                #print(ip)
		status = "validation"
        	if auto_router_login() == True:
			fp = os.path.join(new_folder_name) +"/log.txt"
        		with open(fp, "a") as file:
                		file.write("\n")
                		file.close()
			worksheet.write(j, 3, 'success',style2)
			workbook.save(new_folder_name+'/Result.xls')
                	print ("Authendication success")
		else:
			worksheet.write(j, 3, 'failed',style1)
			workbook.save(new_folder_name+'/Result.xls')
			fp = os.path.join(new_folder_name) +"/log.txt"
                        with open(fp, "a") as file:
                                file.write("Authendication failed on "+host_ip+" \n")
                                file.close()
			print ("Authendication failed")
	else:
		continue
workbook.save(new_folder_name+'/Result.xls')
file_save_path = new_folder_name+'/Result.xlsx'

#dir = "Result"
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



