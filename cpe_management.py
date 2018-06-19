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
print(filee)
print(username)

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
		
		print(tel_res)
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

	tel.write(("show ip int brief | in .75\r").encode('ascii'))
        vlan75_output= tel.read_until("#".encode('ascii'))
	print("vlan75_output=",vlan75_output)
	
	print("hostname", host_name,type(host_name),len(host_name))
	#print("hostname", str(host_name)+"#")
	# tel.write(("sh banner exec\r").encode('ascii'))
	# banner_output = tel.read_until("#".encode('ascii'))
	# print("banner_output", banner_output)
	#
	# tel.write(("sh run | i hostname\r\r").encode('ascii'))
	# time.sleep(.5)
	# print(tel.read_until("#".encode('ascii')))
	
	
	tel.write(("sh run | i hostname\r").encode('ascii'))
	hostname_output = tel.read_until("#".encode('ascii'))
	print("hostname_output",hostname_output)
	
	#print(vlan75_output.decode("utf-8"))
	vlan75_ip = ""
	vlan75 = "False"
	if bool(re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}',vlan75_output.decode("utf-8"))) is True:
		vlan75_ip = re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}',vlan75_output.decode("utf-8")).group()
		print(vlan75_ip)
		vlan75 = "True"
		if host_ip != vlan75_ip:
			worksheet.write(j, 0, vlan75_ip,style2)
        		workbook.save(new_folder_name+'/Result.xls')
		else:
			worksheet.write(j, 0, host_ip,style2)
                        workbook.save(new_folder_name+'/Result.xls')
	else:
		worksheet.write(j, 0, host_ip,style2)
                workbook.save(new_folder_name+'/Result.xls')

	tel.write(("show standby brief | in "+vlan75_ip[:-2]+"\r").encode('ascii'))
        hsrp_output = tel.read_until("#".encode('ascii'))
	print("hsrp_output",hsrp_output)
        tel.write(("show ip eigrp nei | in "+vlan75_ip[:-2]+"\r").encode('ascii'))
        eigrp_output = tel.read_until("#".encode('ascii'))
	
	hsrp = "False"
	hsrp_output_splitlin = hsrp_output.decode("utf-8").splitlines()[1:][:-1]
	
	print("hsrp_output_splitlin",hsrp_output_splitlin)
	if hsrp_output_splitlin and vlan75 == "True":
    		hsrp_output_split = str(hsrp_output_splitlin).split()
    		#print(hsrp_output_split[6],type(hsrp_output_split),len(hsrp_output_split))
    		if bool(re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}',hsrp_output_split[6])) is True and len(hsrp_output_split) > 6:
			worksheet.write(j, 10, hsrp_output_split[6],style2)
			workbook.save(new_folder_name+'/Result.xls')
            		print("success",hsrp_output_split[6])
			hsrp = "True"
    		else:
            		print("fail")
	
	#if hsrp == "False":
	#print(hsrp)
	
	eigrp_splitline = eigrp_output.decode("utf-8").splitlines()[1:][:-1]
	print("eigrp_splitline",eigrp_splitline,len(eigrp_splitline))
	if bool(re.search('% Incomplete command',str(eigrp_splitline))) is not True and hsrp == "False" and len(eigrp_splitline) != 0:
    		s = re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', str(eigrp_splitline)).group()
    		#print(eigrp_output.decode("utf-8"))
		worksheet.write(j, 10, s,style2)
		workbook.save(new_folder_name+'/Result.xls')
    		#print("eigrp",s)

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
	
	
	
	
	
	#print("hostname_output",hostname_output)
	
	
	
	
	
	
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

worksheet.write(0, 0, 'VLAN 75 Address',style1)
worksheet.write(0, 1, 'Telnet enabled?',style1)
worksheet.write(0, 2, 'Reachability',style1)
worksheet.write(0, 3, 'Authendication',style1)
worksheet.write(0, 4, 'Sdn',style1)
worksheet.write(0, 5, 'Tunnel',style1)
worksheet.write(0, 6, 'Eigrp',style1)
worksheet.write(0, 7, 'None',style1)
worksheet.write(0, 8, 'Remarks',style1)
worksheet.write(0, 9, 'AS',style1)
worksheet.write(0, 10, 'Secondary IP',style1)
worksheet.write(0, 11, 'Input IP',style1)
worksheet.write(0, 12, 'CMF NO',style1)
worksheet.write(0, 13, 'Client Name',style1)
worksheet.write(0, 14, 'Host Name',style1)
worksheet.write(0, 15, 'Tunnel Name',style1)
worksheet.write(0, 16, 'Core Router Name',style1)
worksheet.write(0, 17, 'SSH status',style1)
worksheet.write(0, 18, 'connectivity from core',style1)

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
	for index, value in enumerate(list_host):
		if index == 0:
			tunnel_name = value
			worksheet.write(j, 15, tunnel_name, style2)
			workbook.save(new_folder_name + '/Result.xls')
			print(tunnel_name)
		elif index == 1:
			core_router_name = value
			worksheet.write(j, 16, core_router_name, style2)
			workbook.save(new_folder_name + '/Result.xls')
	ssh = "False"
	try:
		ssh=paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		
	
        	ssh.connect(dict_routername[core_router_name], port=22, username=login_username,
                                        password=pswd,
                                        look_for_keys=False, allow_agent=False)
		remote_conn = ssh.invoke_shell()
		remote_conn.send(" term len 0 \n")
		remote_conn.send(" show run int " + tunnel_name + "\n")
		remote_conn.recv(65535)
		time.sleep(.5)
		output = remote_conn.recv(65535)
		print("output", output)
		
		loopback = re.findall('tunnel destination (.+?)\n', output.decode('utf-8'))
		print("loopback", loopback)
		loopback_ip = str(loopback).replace('\\r', '').replace("'", "").replace("[", "").replace("]",
													 "").replace(
			"u", "")
		print(loopback_ip, type(loopback_ip), len(loopback_ip))
		
		
		# print(list_host,type(list_host),len(list_host))
		# host=str(list_host)
		# host_ip=host.replace("'",'').replace('"','').replace("]",'').replace("[",'').replace("u","").replace(",","")
		# print(host_ip)
		# worksheet.write(j, 11, host_ip,style2)
		# workbook.save(new_folder_name+'/Result.xls')
		# if isUp(host_ip) == True:
		# try:
		# tel = telnetlib.Telnet(host_ip)
		core_conn = "False"
		try:
			remote_conn.send(" term len 0 \n")
			remote_conn.send(" telnet " + loopback_ip + " /vrf IPSEC \n")
			
			time.sleep(.5)
			output = remote_conn.recv(65535)
			print("output1", output)
			
			
		
		
			remote_conn.send("cdknoc\n")
			time.sleep(.5)
			output = remote_conn.recv(65535)
			print(output)
			remote_conn.send("vEtEy01fun!\n")
			time.sleep(.5)
			output = remote_conn.recv(65535)
			print(output)
			remote_conn.send("en\n")
			time.sleep(.5)
			output = remote_conn.recv(65535)
			print(output)
			remote_conn.send("har2$tayN\n")
			time.sleep(.5)
			output = remote_conn.recv(65535)
			print("validator *************",output + " *********************")
			if bool(re.search('% Invalid input detected at ',output.decode("utf-8"))) is not True:
				core_conn = "True"
				worksheet.write(j, 18, "Success", style2)
				workbook.save(new_folder_name + '/Result.xls')
			else:
				worksheet.write(j, 18, "Failed", style2)
				workbook.save(new_folder_name + '/Result.xls')
		except:
			print("Not able to login site through core.")
			
		# if core_conn == "True":
		remote_conn.send("show ip int brief | i 75\n")
		time.sleep(.5)
		vlan75_output = remote_conn.recv(65535)
		print("output_int", vlan75_output)
		
		vlan75_ip = ""
		vlan75 = "False"
		if bool(re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', vlan75_output.decode("utf-8"))) is True and core_conn == "True":
			vlan75_ip = re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}',
					      vlan75_output.decode("utf-8")).group()
			print(vlan75_ip)
		
		host_ip = vlan75_ip
		
		remote_conn.send("show run | i hostname\n")
		time.sleep(.5)
		hostname_output = remote_conn.recv(65535)
		
		remote_conn.send("sh banner exec\n")
		time.sleep(.5)
		banner_output = remote_conn.recv(65535)
		
		hostname_find = re.findall('hostname (.+?)\n', hostname_output.decode("utf-8"))
		print(hostname_find, type(hostname_find), len(hostname_find))
		for host_name in hostname_find:
			print(host_name)
		worksheet.write(j, 14, host_name, style2)
		workbook.save(new_folder_name + '/Result.xls')
		
		cmf_no_find = re.findall('Client CMF = (.+?)\n', banner_output.decode("utf-8"))
		print("CMFFFFFFFFF", cmf_no_find)
		cmf_no = str(cmf_no_find).replace("[", "").replace("]", "").replace("u'", "").replace("\\r",
												      "").replace("'",
														  "").strip()
		print(cmf_no)
		worksheet.write(j, 12, cmf_no, style2)
		workbook.save(new_folder_name + '/Result.xls')
		
		client_name_find = re.findall('Client Name = (.+?)\n', banner_output.decode("utf-8"))
		print("client_name_find", client_name_find)
		
		client_name = str(client_name_find).replace("[", "").replace("]", "").replace("u'", "").replace("\\r",
														"").replace(
			"'", "").strip()
		
		print("client_name", client_name)
		worksheet.write(j, 13, client_name, style2)
		workbook.save(new_folder_name + '/Result.xls')
		
		
		if loopback_ip:
			ssh = "True"
		
	except:
		
		print("SSH failed on "+dict_routername[core_router_name])
		
	
	if ssh == "True":
		
		worksheet.write(j, 17, "Success", style2)
		workbook.save(new_folder_name + '/Result.xls')
		
		if isUp(host_ip) == True:
			try:
				tel = telnetlib.Telnet(host_ip)
				worksheet.write(j, 1, 'Enabled', style2)
				workbook.save(new_folder_name + '/Result.xls')
			except:
				worksheet.write(j, 1, 'Not Enabled', style1)
				workbook.save(new_folder_name + '/Result.xls')
				print("please enable telnet")
				continue
			
			# print(ip)
			status = "validation"
			if auto_router_login() == True:
				fp = os.path.join(new_folder_name) + "/log.txt"
				with open(fp, "a") as file:
					file.write("\n")
					file.close()
				worksheet.write(j, 3, 'success', style2)
				workbook.save(new_folder_name + '/Result.xls')
				print("Authendication success 457")
			else:
				worksheet.write(j, 3, 'failed', style1)
				workbook.save(new_folder_name + '/Result.xls')
				fp = os.path.join(new_folder_name) + "/log.txt"
				with open(fp, "a") as file:
					file.write("Authendication failed on " + host_ip + " \n")
					file.close()
				print("Authendication failed 465")
	else:
		
		worksheet.write(j, 17, "Failed", style2)
		workbook.save(new_folder_name + '/Result.xls')
		
		
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



