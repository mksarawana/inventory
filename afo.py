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
import netaddr
from netaddr import *

users_list = ['adpnoc', 'adp']
default_router_password = 'r0adbl0ck'
default_enable_password = 'keep0ut'
rvname = ""
#save_file_path = '/home/sarava/failover/'
primary_ip = []
secondary_ip = []
pri_chk = []
exit = []
server_ip = []
source_interface = []
result_chk = []
acl_subnets = []
vlan_subnets = []
vlan_interfaces = []
extra_interface = []
primary_vlan_interfaces = []
actual_result_chk = []
primary_interface = []
success_interfaces = []
failed_interfaces = []
eigrp_interfaces = []
vrf_name = ["CDK","INTERNET"]
ip1 =  sys.argv[1]
ip2 =  sys.argv[2]
new_folder_name = "/var/www/html/failovertests/uploads/"+ip1+"_"+datetime.datetime.now().strftime("%m-%d-%y_%H-%M-%S")
log_file_path = "/var/www/html/test_tart/failovertests/uploads/"
os.mkdir(new_folder_name)
save_file_path=new_folder_name+"/"
filename = new_folder_name.replace("/var/www/html/failovertests/uploads/","")
#print("filename",filename)
##################### single site ######################
#*******************CPE - FUNCTION BLOCK TO CHECK BETWEEN 2 DIFFERENT LOGIN ACCOUNTS AND GIVE ENABLE ACCESS********************
def auto_router_login(status):
        tryy = 0
	#print("auto done")
        for x in users_list:
                r1_bool = False
                time.sleep(1)
                tel_res = tel.read_until("sername: ".encode('ascii'),2)# Regular login attempt
	#	print(tel_res)
                time.sleep(1)
                tel.write((x + '\r').encode('ascii'))
                tel.read_until('assword: '.encode('ascii'))
                tel.write((default_router_password + '\r' + '\n \n').encode('ascii'))
        #       time.sleep(1.2)
                tryy = tryy + 1
                login_status = tel.read_until(">".encode('ascii'),2)
	#	print(login_status)
                if bool(re.search(">",login_status.decode("utf-8"))) is True:
#                        print("default login success")
                        r1_bool = True
                        enab(status)
                        break
                else:
        #               print "Error Credentials on both the attempts.\n"
                        r1_bool = False
        return r1_bool
#********************CPE - FUNCTION BLOCK TO MANUALLY ENTER THE CUSTOM CLIENT ROUTER CREDENTIALS********************
def manual_router_login(status):
        r2_bool = False
 #       print ("manual login")
        run_time_user_id = raw_input('Please provide the CUSTOM ROUTER USERNAME: ')
        run_time_password = raw_input('Please provide the CUSTOM ROUTER PASSWORD: ')
        #tel = telnetlib.Telnet(vlan75_ip)
        tel.read_until("sername: ".encode('ascii'))# Regular login attempt
        tel.write((run_time_user_id + '\r').encode('ascii'))
        tel.read_until('assword: '.encode('ascii'))
        tel.write((run_time_password + '\r'+'\n \n').encode('ascii'))
        #time.sleep(1.2)
        login_state = tel.read_until(">".encode('ascii'),2)
#       print(login_state.decode("utf-8"))
        if bool(re.search(">",login_state.decode("utf-8"))) is True:
                print ("Manual Login Successful. Need to try ENABLE LOGIN")
                r2_bool = True
                enab(status)

        else:
                print ("Incorrect Credentials. MAXIMUM TRIES REACHED. Exiting in 3.......2.......1..\n")
                r2_bool = False
        #print "r2_bool value is: ", r2_bool
        return r2_bool
#********************CPE - FUNCTION BLOCK FOR DEFAULT ENABLE PASSWORD AUTHENTICATION********************
def enab(status):
        enab_bool = False
        #print ("Trying Enable login now")
        tel.write("en\r".encode('ascii'))
        #print(tel.read_until('assword: '.encode('ascii'),2))
        tel.read_until('assword: '.encode('ascii'),2)
        tel.write((default_enable_password + '\r').encode('ascii'))
        enab_status = tel.read_until("#".encode('ascii'), 2)
        if bool(re.search("#",enab_status.decode("utf-8"))) is True:
              #  print ("Auto ENABLE CREDENTIALS worked!")
                enab_bool = True
#		print("status",status)
		if status == "validation":
                	validation()
		elif status == "post_test":
			actual_test()
		else:
			print("")

        elif bool(re.search("assword:",enab_status.decode("utf-8"))) is True:
                print ("AUTO ENABLE CREDENTIALS DID NOT WORK.")
        #       print "\nCustomer might be having CUSTOM PREVILIDGE PASSWORD. Please refer NETLIB or CRYPTO TOOL to know the password. \n Please enter the password below:\n"
                man_enab_pwd = raw_input('Please enter the CUSTOM ENABLE password here: ')
                tel.read_until('assword: '.encode('ascii'))
                tel.write((man_enab_pwd + '\r').encode('ascii'))
                if tel.read_until("#".encode('ascii'), 2):
        #                       print "Manual ENABLE CREDENTIALS worked! Previlidged access achieved\n\n"
                        enab_bool = True
                        if status == "validation":
                        	validation()
                	elif status == "post_test":
                        	actual_test()
                	else:
                        	print("")

        else:
                print ("ERROR IN CUSTOM ENABLE PASSWORD")
                enab_bool = False
        return enab_bool

#********************CPE - FUNCTION BLOCK TO CHECK IF THE VLAN 75 IP IS RECHABLE FROM THE HOST SYSTEM********************
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
                #print (hostname, 'is up!')
                isUpBool = True
        else:
            	print (hostname, 'is down!')
	return isUpBool
#********************************* Validation **************************************

def validation():
	#print("login ip",ip)
	#print("validating")
	source_interface[:] = []
        server_ip[:] = []
	vlan_subnets[:] = []
	acl_subnets[:] = []
	vlan_interfaces[:] = []
	eigrp_interfaces[:] = []
#*************************** commands ***********************
	tel.write("ter len 0\r".encode('ascii'))
	tel.read_until("#".encode('ascii'))

	tel.write("sh run | i hostname\r".encode('ascii'))
        host_name = tel.read_until("#".encode('ascii'))
	
	tel.write("sh ip interface brief | exc unassigned\r".encode('ascii'))
        pre_test_int_status = tel.read_until("#".encode('ascii'))
		
	tel.write("sh ip eigrp nei\r".encode('ascii'))
        eigrp_status = tel.read_until("#".encode('ascii'))
	
	tel.write("sh ip int brief | i up \r".encode('ascii'))
        active_interface = tel.read_until("#".encode('ascii'))
	#print(active_interface)
	tel.write("Sh route-map NAT-TO-CDK\r".encode('ascii'))
	sec_cmd1 = tel.read_until("#".encode('ascii'))

	tel.write("sh run | in dms|crm\r".encode('ascii'))# to find CRM and DMS IP
        server_ip_result = tel.read_until("#".encode('ascii'))
        tel.write("sh vlans dot1q internal \r".encode('ascii'))# to find source interfaces
        interface_ip_result = tel.read_until("#".encode('ascii'))
	tel.write("show ip eigrp interfaces \r".encode('ascii'))# to find source interfaces
        eigrp_interface_result = tel.read_until("#".encode('ascii'))
	
	#print(eigrp_interface_result.decode("utf-8"),"length",len(eigrp_interface_result))	
	host = re.findall('hostname (.+?)\n',host_name.decode('utf-8'))
        hostname = str(host).replace("[","").replace("]","").replace("u'","").replace("[","").replace("\\r","").replace("'","")	

	if bool(re.search('Interface',eigrp_interface_result.decode("utf-8"))) is not True: #VRF configured routers
		tel.write("sh ip eigrp vrf CDK interfaces \r".encode('ascii'))# to find source interfaces
        	eigrp_interface_result = tel.read_until("#".encode('ascii'))
		if bool(re.search('Interface',eigrp_interface_result.decode("utf-8"))) is not True:
			tel.write("sh ip eigrp vrf INTERNET  interfaces \r".encode('ascii'))# to find source interfaces
                	eigrp_interface_result = tel.read_until("#".encode('ascii'))
	tun_int  = re.findall('interface (.+?)\n',sec_cmd1.decode('utf-8'))
	#print(tun_int,type(tun_int),len(tun_int))

	if len(tun_int) == 0: # to find the interface to shut
		tel.write("Sh route-map NAT-TO-ADP\r".encode('ascii'))
     		sec_cmd2 = tel.read_until("#".encode('ascii'))
		tun_int  = re.findall('interface (.+?)\n',sec_cmd2.decode('utf-8'))
		tel.write("Show ip access-list NAT-TO-ADP\r".encode('ascii'))
	        nat_acl = tel.read_until("#".encode('ascii'))
	 #       print(tun_int,type(tun_int),len(tun_int))
		if len(tun_int) == 0: # adp tunnel interface
			exit.append("NAT-TO CDK and NAT-TO-ADP is not available")
	else:
		tel.write("Show ip access-list NAT-TO-CDK\r".encode('ascii'))
                nat_acl = tel.read_until("#".encode('ascii'))
	nat_subnets = re.findall('permit ip (.+?)\n',nat_acl.decode('utf-8'))
	for sub in nat_subnets:
    		acl_subnets.append(sub)
	interface= str(tun_int).replace("[",'').replace("]",'').replace("u'",'').replace("\\r",'').replace("'","").replace('"','')  #outside interface 
#	interface = str(interface_uni )
       # print("interface:",interface,type(interface),len(interface))
	if bool(re.search(interface+" ",active_interface.decode("utf-8"))) is not True :#to check if the interface is active
		exit.append("tunnel or outside interface is down")

	
			
	if bool(re.search('unnel',interface)) is True : # verify if the interface is tunnel
		eigrp_interface = interface.replace("nnel","")
	#	print("eigrp int",eigrp_interface)
		if bool(re.search(eigrp_interface,eigrp_interface_result.decode("utf-8"))) is not True:
			exit.append("Eigrp is down")
		else:
			print("")
		
		tel.write(("sh run int "+interface+"\r").encode('ascii')) # to find the primary and secondary router ip
                tun_conf = tel.read_until("#".encode('ascii'))
		#print(tun_conf )
                delay_find  = re.findall('delay (.+?)\n',tun_conf.decode('utf-8'))
                delay = str(delay_find).replace("[",'').replace("]",'').replace("u'",'').replace("\\r",'').replace("'","").replace('"','')
                #print("delay",delay,type(delay),len(delay))
		delay_str = str(delay)
		#print("str",type(delay_str ))
                if delay == "100000":
                        primary_ip.append(ip)
                        pri_chk = True
			primary_interface.append(interface)
			#print(ip)
			#secondary_ip = ""
                else:
                        secondary_ip.append(ip)


        else:
                if  len(primary_ip) != 0:
			secondary_ip[:] = []
                        secondary_ip.append(primary_ip)
                #tel.write(("sh run int "+interface+"\r").encode('ascii'))
                #tun_conf = tel.read_until("#".encode('ascii'))
		primary_ip[:] = []
                primary_ip.append(ip)
		primary_interface.append(interface)
	#	print("exit",type(exit))
		str(exit).replace("Eigrp is Down","")
	
	server_ip_find = re.findall("ip host (.+?)\n",server_ip_result.decode('utf-8'))
        #print(server_ip_find,type(server_ip_find))
        for ser in server_ip_find:
                s = re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', ser).group()
                server_ip.append(s)
#        print("server ip",server_ip)
#       for server in server_ip:
#               print(server)
#       print(interface_ip_result)
	fp = os.path.join(log_file_path) +"log.txt"
        with open(fp, "a") as file:
               	file.write('\n'+'pre test on')
                file.close()
	fp = os.path.join(log_file_path) +"log.txt"
        with open(fp, "a") as file:
        	file.write('\n'+'pre test off')
                file.close()
	fp = os.path.join(log_file_path) +"log.txt"
        with open(fp, "a") as file:
        	file.write('\n'+'pre test great')
                file.close()
	print("fp ",fp)

########################## vlan interfaces to test ##########################################################################

	filtter = ["show","EIGRP-IPv4","Xmit","Interface","NV0",hostname+"#"]
	eig_chk = "false"
	exp_outoput = eigrp_interface_result.decode("utf-8").splitlines()
	#print("jkahsjl",eigrp_interface_result.decode("utf-8"))
	for exp in exp_outoput:
    		exp_split = exp.split()
		if len(exp_split) != 0:
    			if bool(re.search(exp_split[0],str(filtter))) is not True and not "Tu" in exp_split[0] and bool(re.search('\.',exp_split[0])) is True:
        		##print(exp_split[0])
				eigrp_interfaces.append(exp_split[0])
	#print("Eigrp interfaces",eigrp_interfaces)
        int_name = re.findall('.1Q, (.+?)\n',interface_ip_result.decode('utf-8')) # show vlans dot1q internal command  reference
	#print("int_name",int_name)
	if len(eigrp_interfaces) != 0:
		eig_chk = "True"
		for inter in eigrp_interfaces:
         #       	print("inter",inter)
                        tel.write(("show run interface " + inter+"\r").encode('ascii'))
                        int_out = tel.read_until("#".encode('ascii'),2)
                        #tel.read_until("#".encode('ascii'))
                        #print(int_out.decode('utf-8'))
                        int_subnet = re.findall('ip address (.+?)\n',int_out.decode('utf-8'))
                        splt = str(int_subnet).split()
        #               print("splt",splt)
                        ip_add = splt[0].replace("['","").replace("[u'","")
                        subnet = splt[1].replace("\\r","").replace("']","")
        #               print("ip_add: ",ip_add)
        #               print("subnet: ",subnet)
                        ip_and_mask = ip_add + "/" + subnet
                        ip_conv = IPNetwork(ip_and_mask)
                        network = ip_conv.network
                        host = ip_conv.hostmask
                        vlan_subnet = str(network) + " "+ str(host)
          #              print(vlan_subnet,type(vlan_subnet))
                        vlan_subnets.append(vlan_subnet)
                        if ip_add == ip:
        #                       print("match found with loin ip")
                                acl_subnets.append(vlan_subnet)
			for acls in acl_subnets:
                        	if bool(re.search(vlan_subnet[:3],acls[:3])) is True:
                                	vlan_interfaces.append(inter)
                        	else:
        #                       	print("failure")
                                	extra_interface.append(inter)

	
	
	elif len(int_name) != 0 and eig_chk == "false":
        	for interface in int_name:
                	source_interface.append(interface.replace(")",""))
        #print(source_interface)
		for inter in source_interface:
	#		print("inter",inter)
   			tel.write(("show run interface " + inter+"\r").encode('ascii'))  
			int_out = tel.read_until("#".encode('ascii'))
			tel.read_until("#".encode('ascii'))
	#		print(int_out.decode('utf-8'))
    			int_subnet = re.findall('ip address (.+?)\n',int_out.decode('utf-8'))
    			splt = str(int_subnet).split()
	#		print("splt",splt)
    			ip_add = splt[0].replace("['","").replace("[u'","")
    			subnet = splt[1].replace("\\r","").replace("']","")
    	#		print("ip_add: ",ip_add)
	#		print("subnet: ",subnet)
   			ip_and_mask = ip_add + "/" + subnet
    			ip_conv = IPNetwork(ip_and_mask)
    			network = ip_conv.network
    			host = ip_conv.hostmask
    			vlan_subnet = str(network) + " "+ str(host)
    	#		print(vlan_subnet,type(vlan_subnet))
    			vlan_subnets.append(vlan_subnet)
    			if ip_add == ip:
        #			print("match found with loin ip")
        			acl_subnets.append(vlan_subnet)
   			for acls in acl_subnets: 
   	 			if bool(re.search(vlan_subnet[:3],acls[:3])) is True:
       					vlan_interfaces.append(inter)
    				else:
        #				print("failure")
        				extra_interface.append(inter)
	else:
		print("interface not found")
		exit.append("Source interfaces not found")
	
    	if ip.replace("['","").replace("[u'","") == str(primary_ip).replace("'","").replace("[","").replace("]",""): # identify the interfaces which we need to do actual test
		#print("make all happy")
		primary_vlan_interfaces.append(vlan_interfaces)

	#print("vlan subnets ",vlan_subnets)
        #print("ACL subnets ",acl_subnets)
	#print("Vlan interfaces",vlan_interfaces)
	print("pre test on: ",ip)	
	fp = os.path.join(save_file_path, ip) +"_pretest"+ '_' +'.txt'
        with open(fp, "a") as file:
        	file.write('\n'+pre_test_int_status.decode('utf-8'))
                file.close()	
        if (len(vlan_interfaces) and len(server_ip) != 0):
                for test_ip in server_ip:
                        #print("test ip ",test_ip)
                        for test_interface in vlan_interfaces:
           #                     print("test_interface ",test_interface)

                                tel.write(("telnet "+ test_ip+" 80 /source-interface "+test_interface+"\r").encode('ascii'))

                                pre_test_result = tel.read_until("Open".encode('ascii'),2)
                                #print(out)
                                fp = os.path.join(save_file_path, ip) +"_pretest"+ '_' +'.txt'
                                with open(fp, "a") as file:
                                        file.write('\n'+pre_test_result.decode('utf-8'))
                                        file.close()
                                if bool(re.search('Open',pre_test_result.decode('utf-8'))) is True:
                                        tel.write('get\r'.encode('ascii'))
                                        tel.read_until("foreign host]".encode('ascii'))
                                        tel.read_until("#".encode('ascii'))
                                        print(pre_test_result.decode('utf-8'))
					result_chk.append("Success")
					success_interfaces.append(test_interface)
                                else:
					tel.read_until("#".encode('ascii'))
                                        print(pre_test_result.decode('utf-8'))
                                        result_chk.append("fail")
					failed_interfaces.append(test_interface)
					if ip.replace("['","").replace("[u'","") == str(primary_ip).replace("'","").replace("[","").replace("]",""):
						exit.append("DMS connectivity issue")
					
					#continue
	tel.write("sh run\r".encode('ascii'))
	tel.write("sh ip eigrp nei\r".encode('ascii'))
	tel.write("sh ip int brief\r".encode('ascii'))
	tel.write("sh ip bgp summary\r".encode('ascii'))
	tel.write("sh vrf\r".encode('ascii'))
	tel.write("wr\r".encode('ascii'))
	tel.write("exit\r".encode('ascii'))
	backup = tel.read_all()
#	print(backup.decode("utf-8"))
#*************************8 writing the output to notepad  ***************************************************	
	fp = os.path.join(save_file_path, ip) +"_backup"+'.txt'
	with open(fp, "a") as file:
        	file.write(backup.decode('utf-8'))
		file.close()


def actual_test():
	#print("Vlan interfaces",primary_vlan_interfaces,type(primary_vlan_interfaces),len(primary_vlan_interfaces))
	#print("Server ip",server_ip,type(server_ip),len(server_ip))
	#print("prinmary_ip",primary_login_ip)
	#print("secondary ip",secondary_login_ip)
	#print("primary interface",primary_interface)	
	shut_interface = str(primary_interface).replace("[","").replace("]","").replace("'","")[1:]
	
	print("shutting the interface",shut_interface+" on "+primary_login_ip)
	tel.write(("ter len 0\r").encode('ascii'))
        tel.read_until("#".encode('ascii'))
	tel.write(("wr\r").encode('ascii'))
	tel.read_until("#".encode('ascii'))
	#tel.write(("reload in 10\r").encode('ascii'))
	#tel.read_until("[confirm]".encode('ascii'))
	#tel.write(("\r").encode('ascii'))
	#tel.read_until("#".encode('ascii'))
	#tel.write(("conf t \r").encode('ascii'))
	#tel.read_until("#".encode('ascii'))
	#tel.write(("interface "+shut_interface+"\r").encode('ascii'))
        #tel.read_until("#".encode('ascii'))
	#tel.write(("shut\r").encode('ascii'))   # to shut the interface
        #tel.read_until("#".encode('ascii'))   
	#tel.write(("end\r").encode('ascii'))
        #tel.read_until("#".encode('ascii'))
	tel.write(("show ip interface brief | exc unassigned\r").encode('ascii'))
        shut_int_status = tel.read_until("#".encode('ascii'))
	#time.sleep(60)
	clean_primary_vlan_interfaces = str(primary_vlan_interfaces).replace("[","").replace("]","").replace("'","").replace("\\r","").replace("u","").split(",")
	print("actual test")
	for test_server_ip in server_ip:
		print("test server ip",test_server_ip)
		for test_vlan_interface in clean_primary_vlan_interfaces:
			#print("test vlan interface",test_vlan_interface,type(test_vlan_interface))
		
			tel.write(("telnet "+ str(test_server_ip)+" 80 /source-interface "+str(test_vlan_interface)+"\r").encode('ascii'))
                	actual_test_result = tel.read_until("Open".encode('ascii'),2)
               #print(out)
     	        	fp = os.path.join(save_file_path, "actual_test")  + '.txt'
                	with open(fp, "a") as file:
		            	file.write('\n'+actual_test_result.decode('utf-8'))
                		file.close()
                	if bool(re.search('Open',actual_test_result.decode('utf-8'))) is True:
                		tel.write('get\r'.encode('ascii'))
                        	tel.read_until("foreign host]".encode('ascii'))
                        	tel.read_until("#".encode('ascii'))
                        	print(actual_test_result.decode('utf-8'))
                        	actual_result_chk.append("Success")
			else:
				tel.read_until("#".encode('ascii'))
                        	print(actual_test_result.decode('utf-8'))
                        	actual_result_chk.append("fail")
                        	continue
	fp = os.path.join(save_file_path, "actual_test")+ '.txt'
        with open(fp, "a") as file:
        	file.write('\n'+shut_int_status.decode("utf-8"))
        	file.close()
	#tel.write(("conf t \r").encode('ascii'))
        #tel.read_until("#".encode('ascii'))
        #tel.write(("interface "+shut_interface+"\r").encode('ascii'))
        #tel.read_until("#".encode('ascii'))
        #tel.write((" no shut\r").encode('ascii'))
        #tel.read_until("#".encode('ascii'))
        #tel.write(("end\r").encode('ascii'))
        #tel.read_until("#".encode('ascii'))
	#tel.write(("wr\r").encode('ascii'))
        #tel.read_until("#".encode('ascii'))
	#time.sleep(60)
        tel.write(("show ip interface brief | exc unassigned\r").encode('ascii'))
	enab_int_status = tel.read_until("#".encode('ascii'))
        tel.write(("reload cancel\r").encode('ascii'))
        reload_status = tel.read_until("#".encode('ascii'))	
	fp = os.path.join(save_file_path, "post_test") +'.txt'
        with open(fp, "w") as file:
        	file.write('\n'.join([reload_status,enab_int_status.decode("utf-8")]))
                file.close()

####################### Execution begins here ####################################

login_ip = [ip1,ip2]
       # print(login_ip,type(login_ip))
for ip in login_ip:
#print(ip)
	if isUp(ip) == True:
             	tel = telnetlib.Telnet(ip)
                #print(ip)
		status = "validation"
        	if auto_router_login(status) == True:
                	print ("")
                else:
                	tel = telnetlib.Telnet(ip)
                        manual_router_login(status)
	else:
		print("ip is not reachable")
#	print("exit",exit,len(exit))
if not exit:
	print("proceeding with post test")
	#print("entered to exit")
	print("pri and sec ip",primary_ip,secondary_ip)
	status = "posttest"
	primary_login_ip = str(primary_ip).replace("'","").replace("[","").replace("]","")
	secondary_login_ip = str(secondary_ip).replace("'","").replace("[","").replace("]","")
	#print(test_login_ip)
#	print("primary vlan interfaces",primary_vlan_interfaces)
	if isUp(secondary_login_ip) == True:
		tel = telnetlib.Telnet(secondary_login_ip)
		if auto_router_login(status) == True:
                        print ("")
                else:
                        tel = telnetlib.Telnet(secondary_login_ip)
                        manual_router_login(status)
        else:
                print("ip is not reachable")	
	tel.write("ter len 0\r".encode('ascii'))
        tel.read_until("#".encode('ascii'))

#        tel.write(("telnet "+primary_login_ip+"\r").encode('ascii'))
        if isUp(primary_login_ip) == True:
                tel.write(("telnet "+primary_login_ip+"\r").encode('ascii'))
		tel_res = tel.read_until("#".encode('ascii'),2)
	#	print(tel_res)
		if bool(re.search('Open',tel_res.decode("utf-8"))) is not True:
			print("logging in using VRF please wait for 10 seconds...")
                        for vname in vrf_name:
                                tel.write(("telnet "+primary_login_ip+" /vrf "+vname+"\r").encode('ascii'))
				time.sleep(2)
                                tel_res = tel.read_until("#".encode('ascii'),2)
				#tel.write(("exit \r").encode('ascii'))
				#tel.read_all()
				#print("tel resss",tel_res)
				tel.read_until("#".encode('ascii'))
                                if bool(re.search('Open',tel_res.decode("utf-8"))) is not True:
					#print("vrf name", vname)
					#rvname = vname
					continue
				else:
					#print("vrf name", vname)
                                        rvname = vname
			tel.write(("telnet "+primary_login_ip+" /vrf "+rvname+"\r").encode('ascii'))
		#print("vname",rvname)
	#	else:
	#		tel.write(("telnet "+primary_login_ip+"\r").encode('ascii'))	
                #print("going to real test")
                status = "post_test"
                if auto_router_login(status) == True:
                        print ("")
                else:
                        tel.write(("telnet "+primary_login_ip+"\r").encode('ascii'))
                        manual_router_login(status)
        else:
                print("ip is not reachable")
else:
	print("something went wrong.... possible reasons: ",exit)
#zip = "cd /var/www/html/failovertests/uploads/; ""tar -zcvf "+new_folder_name+".tar.gz " +new_folder_name+"/"+";"+" mv "+new_folder_name+".tar.gz /var/www/html/failovertests/logs/"" 2> /dev/null"
#os.system(zip)
dir = new_folder_name.replace("/var/www/html/failovertests/uploads/","")
dir_name = dir+"/"
zip = "cd /var/www/html/failovertests/uploads/; tar -zcvf %s.tar.gz %s; cp %s.tar.gz /var/www/html/failovertests/logs/ 2> /dev/null" %(dir,dir_name,dir)
os.system(zip)
save_path = "/var/www/html/failovertests/logs/"
print("File saved path : ",save_path,filename+".tar.gz")

	
