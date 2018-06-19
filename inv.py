#!/usr/bin/python
from __future__ import unicode_literals
from __future__ import print_function
import sys
import telnetlib
import paramiko
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
import glob
import re


users_list = ['cdknoc', 'adp']
default_router_password = 'vEtEy01fun!'
default_enable_password = 'har2$tayN'
remarks = []
output_file_name = ""
vrf_name = ""
login_hosts = []

dict_routername=  { "ORD1-ACCESSR15" : "100.76.255.120",   "ORD1-ACCESSR16" : "100.76.255.119",
                    "ORD1-ACCESSR01" : "100.76.255.227" , "ORD1-ACCESSR02" :  "100.76.255.226",
                    "ORD1-ACCESSR03" :  "100.76.255.225",   "ORD1-ACCESSR04" : "100.76.255.224",
                     "ORD1-ACCESSR05" : "100.76.255.223",   "ORD1-ACCESSR06" : "100.76.255.222",
                     "ORD1-ACCESSR07" : "100.76.255.221",  "ORD1-ACCESSR08" : "100.76.255.220",
                   "ORD1-ACCESSR09": "100.76.255.219",
                   "LAS-ACCESSR01" : "100.80.255.227" ,   "LAS-ACCESSR02" : "100.80.255.226",
                    "LAS-ACCESSR03"  :"100.80.255.225",   "LAS-ACCESSR04" : "100.80.255.224",
                     "LAS-ACCESSR05" : "100.80.255.223",  "LAS-ACCESSR06" : "100.80.255.222" ,
                    "LAS-ACCESSR07" : "100.80.255.220" ,  "LAS-ACCESSR08" : "100.80.255.220",
		    "LAS-ACCESSR09" : "100.76.255.219"}


username = sys.argv[2]
filee = sys.argv[1]
# print(filee
# print(username)

login_username = 'admin'
pswd = 'DC21nstall'
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
			login_username = x
                        r1_bool = True
                        if enab(login_username) == True:
                        	break
			else:
				r1_bool = False
                else:
        #               print "Error Credentials on both the attempts.\n"
                        r1_bool = False
        return r1_bool

def enab(login_username):
        enab_bool = False
        #print ("Trying Enable login now")
        tel.write("en\r".encode('ascii'))
        #print(tel.read_until('assword: '.encode('ascii'),2))
        tel.read_until('assword: '.encode('ascii'),2)
        tel.write((default_enable_password + '\r').encode('ascii'))
        enab_status = tel.read_until("#".encode('ascii'), 2)
	#print(enab_status)
        if bool(re.search("#",enab_status.decode("utf-8"))) is True:
                #print ("Auto ENABLE CREDENTIALS worked!")
                enab_bool = True
		if login_status == "Global":
			toc()
		elif login_status == "Local" and len(vrf_name) ==0 : # telnet from tha main router
			print("Local without VRF")
			tel.write(('telnet '+login_ip+  ' \r').encode('ascii'))
			tel.read_until("sername:".encode('ascii'))
			tel.write((login_username+'\r').encode('ascii'))
			tel.read_until("assword:".encode('ascii'))
			tel.write((default_router_password+'\r').encode('ascii'))
			tel.read_until(">".encode('ascii'))
			tel.write(('en \r').encode('ascii'))
			tel.read_until("assword:".encode('ascii'))
			tel.write((default_enable_password+'\r').encode('ascii'))
			tel.read_until("#".encode('ascii'))
			toc()
		elif login_status == "Local" and len(vrf_name) !=0 : # telnet from tha main router
			print("Local with VRF")
			tel.write(('telnet '+login_ip+  'vrf '+vrf_name+' \r').encode('ascii'))
			tel.read_until("sername:".encode('ascii'))
			tel.write((login_username + '\r').encode('ascii'))
			tel.read_until("assword:".encode('ascii'))
			tel.write((default_router_password + '\r').encode('ascii'))
			tel.read_until(">".encode('ascii'))
			tel.write(('en \r').encode('ascii'))
			tel.read_until("assword:".encode('ascii'))
			tel.write((default_enable_password + '\r').encode('ascii'))
			tel.read_until("#".encode('ascii'))
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
	isUpBool = ""
	if login_status == "Global":
		
		if platform.system() == "Windows":
		 #       print ("Pinging Windows")
			response = os.system("ping "+hostname+"> /dev/null")
	 #               print ("\nPing from WINDOWS PC is successful. \nThe client " + hostname + " is LIVE!\n")
		else:
		  #      print ("Pinging Linux")
			response = os.system("ping -c 1 "+hostname+" > /dev/null")
	   #             print ("\nPing from LINUX PC is successful. \nThe client " + hostname + " is LIVE!\n")
		
		if response == 0:
			# worksheet.write(j, 17, 'success',style2)
			# workbook.save(new_folder_name + '/' + output_file_name)
			print (hostname, 'is up!')
			isUpBool = True
		else:
			# worksheet.write(j, 17, 'failed',style1)
			# workbook.save(new_folder_name + '/' + output_file_name)
			print (hostname, 'is down!')
	else:
		isUpBool = True
		
	return isUpBool
################################ Type of connectivity ########################################
def toc():
	sdn = []
	
	tel.write("ter len 0 \r".encode('ascii'))
        tel.read_until("#".encode('ascii'))
	tel.write(('sh vlans | i Virtual LAN ID: | IP\r').encode('ascii'))
        vlan_result = tel.read_until("#".encode('ascii'))
	tel.write(('sh ip int brief | i Vlan\r').encode('ascii'))
	sw_vlan_result = tel.read_until("#".encode('ascii'))
	tel.write("sh run | i hostname \r".encode('ascii'))
	hostname_output = tel.read_until("#".encode('ascii'))
	tel.write("sh cdp nei detail | i Interface:|Device ID:|IP address: \r".encode('ascii'))
	cdp_output = tel.read_until("#".encode('ascii'))
	tel.write("sh vlans | i vLAN Trunk Interface: \r".encode('ascii'))
	trunk_interface_output = tel.read_until("#".encode('ascii'))
	tel.write("sh ip int brief | exc administratively \r".encode('ascii'))
	interface_brief_output = tel.read_until("#".encode('ascii'))
	
	dummy_hostname_find = hostname_output.decode("utf-8").splitlines()
	print("dummy_hostname_find", dummy_hostname_find, type(dummy_hostname_find), len(dummy_hostname_find))
	if len(dummy_hostname_find) == 3:
		dummy_hostname = dummy_hostname_find[-1]
		print("dummy", dummy_hostname, type(dummy_hostname), len(dummy_hostname))
		tel.write("sh inv\r".encode('ascii'))
		inventory_output = tel.read_until(dummy_hostname)
		print("inventory_output", inventory_output)
	else:
		print("command execution error")
	tel.write("sh run | be banner exec \r".encode('ascii'))
	banner_output = tel.read_until("end".encode('ascii'))
	print(banner_output)
	# tel.write("\r".encode('ascii'))
	# print("kpppaaaa",tel.read_until("#".encode('ascii')))
	# tel.write("\r".encode('ascii'))
	# print("kpppaaaa", tel.read_until("#".encode('ascii')))
	
	#print(hostname_output)
	#
	
	
	hostname_find = re.findall('hostname (.+?)\n',hostname_output.decode("utf-8"))
	#print("hostname_find",hostname_find)
	# for hostname in hostname_find:
	# 	print(hostname,type(hostname),len(hostname) )
	#print(hostname)
	
	pid_find = re.findall('PID: (.+?),',inventory_output.decode("utf-8") )
	#print(pid_find)
	
	sn_find = re.findall('SN: (.+?)\n', inventory_output.decode("utf-8"))
	#print(sn_find)
	
	
	
	#vlan_id_find = []
	vlan_id_find = re.findall('Virtual LAN ID: (.+?) ()',vlan_result.decode("utf-8")) # Need to ignore first value
	vlan_ip_find = re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', vlan_result.decode("utf-8"))
	vlan_id_find= str(vlan_id_find[1:]).replace(',','')
	#print(vlan_ip_find)
	#print(vlan_id_find)
	
	#print('trun_interface_output', trunk_interface_output)
	
	trunk_interfaces = re.findall('vLAN Trunk Interface: (.+?)\n', trunk_interface_output.decode("utf-8"))
	trunk_interfaces = trunk_interfaces[1:]
	#print('trunk_interfaces', trunk_interfaces)
	
	router_interfaces = []
	used_interface = []
	non_used_interface = []
	no_need_interfaces = ["NVI0",'Loopback',"Interface"]
	if trunk_interfaces:
		interface_brief_output_extract = interface_brief_output.decode("utf-8").splitlines()[1:][:-1]
		for interface in interface_brief_output_extract:
			if len(interface) >2 and bool(re.search("Loopback",interface)) is not True:
				catch = interface.split()
				router_interfaces.append(catch[0])
			
		#print(router_interfaces,type(router_interfaces),len(router_interfaces))
		
		# for ints in router_interfaces:
		# 	print("ints",ints)
		# 	for inters in trunk_interfaces:
		# 		print("inters",inters)
		# 		if ints == inters:
		# 			used_interface.append(ints)
		# 		else:
		# 			non_used_interface.append(ints)
		#
		# print('used_interface',used_interface)
		# print('no used_interface', non_used_interface)
		
		# first_set = list(set(router_interfaces) - set(trunk_interfaces))
		# print('first_set',first_set)
		
		
		for ints in router_interfaces:
			if bool(re.search(ints,str(trunk_interfaces))) is not True:
				non_used_interface.append(ints)
		for inters in non_used_interface:
			# print(inters)
			# print(str(non_used_interface))
			if bool(re.search(inters, str(no_need_interfaces))) is not True:
				
				
				used_interface.append(inters)
		#print('used_interface', used_interface)
		
	sw_vlan_id = []
	unassiged_vlan = []
	assigned_vlan = []
	if not vlan_ip_find:
		#print('sw_vlan_result',sw_vlan_result)
		sw_vlan_result_extract = sw_vlan_result.splitlines()[1:][:-1]
		#print(sw_vlan_result_extract)
		for vln in sw_vlan_result_extract:
			if bool(re.search('unassigned',vln,re.I)) is True:
				unassiged_vlan.append(vln)
			else:
				assigned_vlan.append(vln)
		for vlan in str(assigned_vlan).replace(',','').split():
			if bool(re.search('Vlan',vlan,re.I)) is True:
				sw_vlan_id.append(vlan.replace('[','').replace("'",""))
		vlan_id_find = sw_vlan_id
		#vlan_id_find = vlan_id_find[1:]
			 
				
			
		sw_vlan_ip = re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', str(assigned_vlan))
		vlan_ip_find = sw_vlan_ip
		#print(sw_vlan_ip,type(sw_vlan_ip),len(sw_vlan_ip))
		#print(vlan_ip_find.append(sw_vlan_ip))
		
		
		print("vlan_id_find",vlan_id_find,type(vlan_id_find))
		
	cdp_interfaces = re.findall('Interface: (.+?),',cdp_output.decode("utf-8")) # Interface Information (Used / Available)
	cdp_device_id = re.findall('Device ID: (.+?)\n',cdp_output.decode("utf-8"))  # Uplinked to (Description)
	cdp_ip_address = re.findall('IP address: (.+?)\n',cdp_output.decode("utf-8"))  # column L
	
	#print("cdp_interfaces",cdp_interfaces)
	#print("cdp_device_id", cdp_device_id)
	#print("cdp_ip_address", cdp_ip_address)
	for cdint in used_interface:
		cdp_interfaces.append(cdint)
	#print(cdp_interfaces)
	
	
	
	cmf_no_find = re.findall('Client CMF = (.+?)\n',banner_output.decode('utf-8'))
	site_name_find = re.findall('Client Name = (.+?)\n', banner_output.decode('utf-8'))
	
	#print(cmf_no_find,site_name_find)
	
	
	# trun_interface_output_extract = trun_interface_output.decode("utf-8").splitlines()[1:][:-1]
	# for trunk in str(trun_interface_output_extract).split():
	
	
	excel_formating(cmf_no_find,site_name_find,vlan_id_find,vlan_ip_find,hostname_find,pid_find,sn_find,cdp_interfaces,cdp_device_id,cdp_ip_address,used_interface)

################################## Excel formating #######################################
def excel_formating(cmf_no_find,site_name_find,vlan_id_find,vlan_ip_find,hostname_find,pid_find,sn_find,cdp_interfaces,cdp_device_id,cdp_ip_address,used_interface):
	print("lets format")
	print(position)
	
	print("j",j)
	print("cmf_no_find",cmf_no_find, type(cmf_no_find), len(cmf_no_find))
	print("site_name_find", site_name_find, type(site_name_find), len(site_name_find))
	print("vlan_id_find", vlan_id_find, type(vlan_id_find), len(vlan_id_find))
	print("vlan_ip_find", vlan_ip_find, type(vlan_ip_find), len(vlan_ip_find))
	print("hostname_find", hostname_find, type(hostname_find), len(hostname_find))
	print("pid_find", pid_find, type(pid_find), len(pid_find))
	print("sn_find", sn_find, type(sn_find), len(sn_find))
	print("cdp_interfaces", cdp_interfaces, type(cdp_interfaces), len(cdp_interfaces))
	print("cdp_device_id", cdp_device_id, type(cdp_device_id), len(cdp_device_id))
	print("cdp_ip_address",cdp_ip_address, type(cdp_ip_address), len(cdp_ip_address))
	#print("vlan_id_find", vlan_id_find, type(vlan_id_find), len(vlan_id_find))
	# print(vlan_ip_find, type(vlan_ip_find), len(vlan_ip_find))
	# print(pid_find)
	worksheet.write(position, 0, cmf_no_find, style2)
	worksheet.write(position, 1, site_name_find, style2)
	worksheet.write(position, 3, vlan_ip_find, style2)
	worksheet.write(position, 2, vlan_id_find, style2)
	
	worksheet.write(position, 4, hostname_find, style2)
	worksheet.write(position, 5, pid_find, style2)
	worksheet.write(position, 7,sn_find, style2)
	#worksheet.write(position, 8, used_interface, style2)
	worksheet.write(position, 8, cdp_interfaces, style2)
	worksheet.write(position, 9, cdp_device_id, style2)
	worksheet.write(position, 10, 'Circuit Detail', style2)
	worksheet.write(position, 11, cdp_ip_address, style2)
	
	
	
	#worksheet.write(position, 13, cdp_ip_address, style2)
	workbook.save(new_folder_name + '/' + output_file_name)

################################## Write excel #######################################
new_folder_name = "/var/www/html/test_tart/inventory/uploads/"+username
if not os.path.exists(new_folder_name):
        os.mkdir(new_folder_name)
        fp = os.path.join(new_folder_name) +"/log.txt"
        with open(fp, "a") as file:
                file.write("\n")
                file.close()

move_input_file = "cd /var/www/html/test_tart/inventory/uploads; mv " + filee + " " + new_folder_name + "/"
#print("ads", move_input_file)
os.system(move_input_file)
# zip = "cd  "
# new_folder_name

#print('var/www/html/test_tart/inventory/' + filee)
file_path = os.path.join(new_folder_name + '/', filee)
#print("file path", file_path)
################################## Read excel #################################
book = xlrd.open_workbook(file_path, "r")
first_sheet = book.sheet_by_index(0)
row_count = first_sheet.nrows
#print(first_sheet)
################################## Write excel #################################

workbook = xlwt.Workbook()
worksheet = workbook.add_sheet('Result', cell_overwrite_ok=True)

style0 = xlwt.easyxf('alignment: horiz left; font: bold on , height 320 , color blue;  borders: left medium, top medium, bottom medium; ')# for Dealership name
style1 = xlwt.easyxf('pattern: pattern solid, fore_colour light_green; alignment: horiz centre; font: bold on , height 220')# for header
style2 = xlwt.easyxf('alignment: horiz centre; font: height 220 ')# for router output entries

# book = with open(file_path,"rb") as xlsfile


for j in range(2, row_count):
	#print(j)
	
	list_host = first_sheet.row_values(j)
	for index, value in enumerate(list_host):
		if index == 0:
			host_ip = value
			worksheet.write(j, 15, host_ip, style2)
			
			login_hosts.append(host_ip)
			#print(host_ip)
		elif index == 1:
			print(output_file_name)
			if not output_file_name:
				output_file_name = value + '.xls'
				workbook.save(new_folder_name + '/' + output_file_name)
			# 	worksheet.write(j, 16, core_router_name, style2)
			# 	workbook.save(new_folder_name + '/Result.xls')
		elif index == 2:
			if not vrf_name:
				vrf_name = value
				#print(value)
#print(login_hosts, output_file_name,vrf_name)



#print(worksheet)


#***************** creating header **************************
worksheet.write_merge(0, 0, 0, 3, 'Automotive Group',style0)

worksheet.write(1, 0, 'Client CMF#',style1)
worksheet.write(1, 1, 'Site Name',style1)
worksheet.write(1, 2, 'VLAN',style1)
worksheet.write(1, 3, 'IP-Address',style1)
worksheet.write(1, 4, 'Host Name',style1)
worksheet.write(1, 5, 'Equip Model (PID)',style1)
worksheet.write(1, 6, 'Cards/Modules',style1)
worksheet.write(1, 7, 'Equipment S/N',style1)
worksheet.write(1, 8, 'Interface Information (Used/Available)',style1)
worksheet.write(1, 9, 'Uplinked to (description)',style1)
worksheet.write(1, 10, 'Circuit Detail',style1)
worksheet.write(1, 11, '',style1)
worksheet.write(1, 12, '',style1)
worksheet.write(1, 13, 'Telnet Enabled?',style1)
worksheet.write(1, 14, 'Authentication',style1)
worksheet.write(1, 15, '',style1)
worksheet.write(1, 16, '',style1)
worksheet.write(1, 17, '',style1)
worksheet.write(1, 18, '',style1)

workbook.save(new_folder_name+'/'+output_file_name)





for index,login_ip in enumerate(login_hosts):
	print("k",index)
	position = index+2
	if index == 0:
		primary_login_ip = login_ip
	
	#print(login_ip,type(login_ip),len(login_ip))
	login_ip_i = login_ip[:-2]
	#print("login_ip_i",login_ip_i)
	if bool(re.search(login_ip[:-2],login_hosts[0] )) is True:
		login_status = "Global"
	else:
		login_status = "Local"
	#print("login_status",login_status)

	if isUp(login_ip) == True:
		try:
			if login_status == "Local":
				print("primary_login_ip",primary_login_ip)
				tel = telnetlib.Telnet(primary_login_ip)
				worksheet.write(position, 13, 'Enabled', style2)
				workbook.save(new_folder_name + '/' + output_file_name)
			elif login_status == "Global":
				tel = telnetlib.Telnet(login_ip)
				worksheet.write(position, 13, 'Enabled', style2)
				workbook.save(new_folder_name + '/' + output_file_name)
		except:
			worksheet.write(position, 13, 'Not Enabled', style1)
			workbook.save(new_folder_name + '/' + output_file_name)
			#print("please enable telnet")
			continue

		# print(ip)
		
		if auto_router_login() == True:
			worksheet.write(position, 14, 'success', style2)
			workbook.save(new_folder_name + '/' + output_file_name)
			fp = os.path.join(new_folder_name) + "/log.txt"
			with open(fp, "a") as file:
				file.write("\n")
				file.close()
			
			#print("Authendication success 457")
		else:
			worksheet.write(position, 14, 'failed', style1)
			workbook.save(new_folder_name + '/' + output_file_name)
			fp = os.path.join(new_folder_name) + "/log.txt"
			with open(fp, "a") as file:
				file.write("Authendication failed on " + host_ip + " \n")
				file.close()
			#print("Authendication failed 465")

	
	
	# worksheet.write(j, 1, 'Enabled',style2)
	# workbook.save(new_folder_name+'/Result.xls')
	# except:
	# 	worksheet.write(j, 1, 'Not Enabled',style1)
	# 	workbook.save(new_folder_name+'/Result.xls')
	# 	print("please enable telnet")
	# 	continue
		
		#print(ip)
	# status = "validation"
	# if auto_router_login() == True:
	# 	fp = os.path.join(new_folder_name) +"/log.txt"
	# 	with open(fp, "a") as file:
	# 		file.write("\n")
	# 		file.close()
	# 	worksheet.write(j, 3, 'success',style2)
	# 	workbook.save(new_folder_name+'/Result.xls')
	# 	print ("Authendication success")
	# else:
	# 	worksheet.write(j, 3, 'failed',style1)
	# 	workbook.save(new_folder_name+'/Result.xls')
	# 	fp = os.path.join(new_folder_name) +"/log.txt"
	# 	with open(fp, "a") as file:
	# 		file.write("Authendication failed on "+host_ip+" \n")
	# 		file.close()
	# 	print ("Authendication failed")

workbook.save(new_folder_name+'/'+output_file_name)
file_save_path = new_folder_name+'/'+output_file_name+'x'

#dir = "Result"
download_path = new_folder_name.replace("uploads","logs")
dir = new_folder_name.replace("/var/www/html/test_tart/inventory/uploads/","")
dir_name = dir+"/"
zip = "cd /var/www/html/test_tart/inventory/uploads/; tar -zcvf %s.tar.gz %s; cp %s.tar.gz /var/www/html/test_tart/inventory/logs/ > /dev/null" %(dir,dir_name,dir)
os.system(zip)
#dir_name = '/var/www/html/test_tart/failovertests'
#zip = "cd /var/www/html/test_tart/failovertests/; tar -zcvf %s.tar.gz %s; cp %s.tar.gz /var/www/html/failovertests/logs/ 2> /dev/null" %(dir,dir_name,dir)
#os.system(zip)
#print("File saved path : ",file_save_path)

print("File saved path : ",download_path+".tar.gz")



