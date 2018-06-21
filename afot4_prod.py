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
import requests

users_list = []
default_router_password = ''
default_enable_password = ''
rvname = ""
# save_file_path = '/home/sarava/failover/'
temp_array = []
fstip = []
secip = []
temp_ip = []
primary_ip = []
secondary_ip = []
first_delay = []
second_delay = []
fstint = []
secint = []
fstvlanint = []
secvlanint = []
pri_chk = []
exit = []
server_ip = []
source_interface = []
success_server = []
actual_server = []
pre_result_chk = []
pre_test_resss = ""
acl_subnets = []
vlan_subnets = []
vlan_interfaces = []
extra_interface = []
lan_interfaces = []
primary_vlan_interfaces = []
secondary_vlan_interfaces = []
actual_result_chk = []
primary_interface = []
success_interfaces = []
failed_interfaces = []
eigrp_interfaces = []
vrf_names = ["CDK", "INTERNET", "Mgmt-intf", "ORD", "LAS"]
act_vrf_name = []
vrf_aware = []
fstvrfaware = []
secvrfaware = []
primary_vrf_aware = []
vrf_temp = []
vrf_name = ""

ip1 = sys.argv[1]
ip2 = sys.argv[2]
filenam = sys.argv[3]
# print(filenam)
new_folder_name = "/var/www/html/failovertests/uploads/" + filenam
if not os.path.exists(new_folder_name):
        os.mkdir(new_folder_name)
# print("folder created")
save_file_path = new_folder_name + "/"
filename = new_folder_name.replace("/var/www/html/failovertests/uploads/", "")
fp = os.path.join(save_file_path) + "log.txt"
with open(fp, "a") as file:
        # file.write('Authentication success on: '+ip+'\n')
        file.close()


# print("log file created on ",fp)
# print("filename",filename)

#################################### timer funtionality ###############################

def cls():
        os.system('clear')


def clock():
        hour = 1
        minute = 0
        second = 0
        timeday = 1
        day = ('am')
        while True:
                print(second)
                time.sleep(0.99)
                cls()
                second += 1
                if second == 5:
                        break


# clock()
##################### single site ######################
# *******************CPE - FUNCTION BLOCK TO CHECK BETWEEN 2 DIFFERENT LOGIN ACCOUNTS AND GIVE ENABLE ACCESS********************
def auto_router_login(status):
        tryy = 0
        for x in users_list:
                r1_bool = False
                time.sleep(1)
                tel_res = tel.read_until("sername: ".encode('ascii'), 2)  # Regular login attempt
                time.sleep(1)
                tel.write((x + '\r').encode('ascii'))
                tel.read_until('assword: '.encode('ascii'))
                tel.write((default_router_password + '\r' + '\n \n').encode('ascii'))
                tryy = tryy + 1
                login_status = tel.read_until(">".encode('ascii'), 2)
                if bool(re.search(">", login_status.decode("utf-8"))) is True:
                        r1_bool = True
                        enab(status)
                        break
                else:
                        print("username '" + x + "' did not work on: " + ip)
                        fp = os.path.join(save_file_path) + "log.txt"
                        with open(fp, "a") as file:
                                file.write("username " + x + " did not work \n")
                                file.close()
                        r1_bool = False
        return r1_bool


# ********************CPE - FUNCTION BLOCK TO MANUALLY ENTER THE CUSTOM CLIENT ROUTER CREDENTIALS********************
def manual_router_login(status):
        r2_bool = False
        #       print ("manual login")
        run_time_user_id = raw_input('Please provide the CUSTOM ROUTER USERNAME: ')
        run_time_password = raw_input('Please provide the CUSTOM ROUTER PASSWORD: ')
        # tel = telnetlib.Telnet(vlan75_ip)
        tel.read_until("sername: ".encode('ascii'))  # Regular login attempt
        tel.write((run_time_user_id + '\r').encode('ascii'))
        tel.read_until('assword: '.encode('ascii'))
        tel.write((run_time_password + '\r' + '\n \n').encode('ascii'))
        # time.sleep(1.2)
        login_state = tel.read_until(">".encode('ascii'), 2)
        #       print(login_state.decode("utf-8"))
        if bool(re.search(">", login_state.decode("utf-8"))) is True:
                print("Manual Login Successful. Need to try ENABLE LOGIN")
                r2_bool = True
                enab(status)
        
        else:
                print("Incorrect Credentials. MAXIMUM TRIES REACHED. Exiting in 3.......2.......1..\n")
                r2_bool = False
        # print "r2_bool value is: ", r2_bool
        return r2_bool


# ********************CPE - FUNCTION BLOCK FOR DEFAULT ENABLE PASSWORD AUTHENTICATION********************
def enab(status):
        enab_bool = False
        # print ("Trying Enable login now")
        tel.write("en\r".encode('ascii'))
        # print(tel.read_until('assword: '.encode('ascii'),2))
        tel.read_until('assword: '.encode('ascii'), 2)
        tel.write((default_enable_password + '\r').encode('ascii'))
        enab_status = tel.read_until("#".encode('ascii'), 2)
        if bool(re.search("#", enab_status.decode("utf-8"))) is True:
                print("Athentication success on: ", ip)
                
                fp = os.path.join(save_file_path) + "log.txt"
                with open(fp, "a") as file:
                        file.write('Authentication success on: ' + ip + '\n')
                        file.close()
                enab_bool = True
                #		print("status",status)
                if status == "validation":
                        validation()
                elif status == "post_test":
                        actual_test()
                else:
                        print("")
        else:
                print("ERROR IN ENABLE PASSWORD on: ", ip)
                fp = os.path.join(save_file_path) + "log.txt"
                with open(fp, "a") as file:
                        file.write('ERROR IN ENABLE PASSWORD on: ' + ip + '\n')
                        file.close()
                exit.append("ENABLE CREDENTIALS DID NOT WORK on ip: " + ip)
                # print("exit enable",exit)
                enab_bool = False
        return enab_bool


# ********************CPE - FUNCTION BLOCK TO CHECK IF THE VLAN 75 IP IS RECHABLE FROM THE HOST SYSTEM********************
def isUp(hostname):
        response = ""
        #	print(hostname)
        if platform.system() == "Windows":
                #       print ("Pinging Windows")
                response = os.system("ping " + hostname + "> /dev/null")
                #               print ("\nPing from WINDOWS PC is successful. \nThe client " + hostname + " is LIVE!\n")
        else:
                #      print ("Pinging Linux")
                response = os.system("ping -c 1 " + hostname + " > /dev/null")
                #             print ("\nPing from LINUX PC is successful. \nThe client " + hostname + " is LIVE!\n")
        isUpBool = ""
        if response == 0:
                # print (hostname, 'is up!')
                isUpBool = True
        else:
                print(hostname, 'is down!')
        return isUpBool


# ********************************* Validation **************************************

def validation():
        # print("login ip",ip)
        # print("validating")
        # print("fstvlanint",fstvlanint)
        # print("temp array",temp_array)
        source_interface[:] = []
        server_ip[:] = []
        vlan_subnets[:] = []
        acl_subnets[:] = []
        # vlan_interfaces[:] = []
        eigrp_interfaces[:] = []
        lan_interfaces[:] = []
        interface = ""
        # print("primary vlan",primary_vlan_interfaces,type(primary_vlan_interfaces),len(primary_vlan_interfaces))
        # *************************** commands ***********************
        tel.write("ter len 0\r".encode('ascii'))
        tel.read_until("#".encode('ascii'))
        
        tel.write("sh run | i hostname\r".encode('ascii'))
        host_name = tel.read_until("#".encode('ascii'))
        #print(host_name) 
        tel.write("sh ip interface brief | exc unassigned\r".encode('ascii'))
        pre_test_int_status = tel.read_until("#".encode('ascii'))
        #print(pre_test_int_status) 
        tel.write("sh ip eigrp nei\r".encode('ascii'))
        eigrp_status = tel.read_until("#".encode('ascii'))
        #print(eigrp_status) 
        tel.write("sh run | sec bgp\r".encode('ascii'))
        bgp_config = tel.read_until("#".encode('ascii'))
        #print(bgp_config) 
        tel.write("sh ip bgp summ\r".encode('ascii'))
        bgp_status = tel.read_until("#".encode('ascii'))
        #print(bgp_status) 
        tel.write("sh ip int brief | i down \r".encode('ascii'))
        down_interface = tel.read_until("#".encode('ascii'))
        # print(active_interface)
        print() 
        tel.write("show vrf \r".encode('ascii'))
        vrf_ouput = tel.read_until("#".encode('ascii'))
        
        tel.write("Sh route-map NAT-TO-CDK\r".encode('ascii'))
        sec_cmd1 = tel.read_until("#".encode('ascii'))
        
        tel.write("sh run | in dms|crm\r".encode('ascii'))  # to find CRM and DMS IP
        server_ip_result = tel.read_until("#".encode('ascii'))
        tel.write("sh vlans dot1q internal \r".encode('ascii'))  # to find source interfaces
        interface_ip_result = tel.read_until("#".encode('ascii'))
        tel.write("show ip eigrp interfaces \r".encode('ascii'))  # to find source interfaces
        eigrp_interface_result = tel.read_until("#".encode('ascii'))
        #tel.write("show log \r".encode('ascii'))  # to find source interfaces
        #router_log = tel.read_until("#".encode('ascii'),5)
        #print(tel.read_until("#".encode('ascii')))
        #fp = os.path.join(save_file_path) + "router_logs.txt"
        #with open(fp, "a") as file:
         #       file.write('\n' + router_log.decode('utf-8'))
          #      file.close()
        
        # print(eigrp_interface_result.decode("utf-8"),"length",len(eigrp_interface_result))
        host = re.findall('hostname (.+?)\n', host_name.decode('utf-8'))
        hostname = str(host).replace("[", "").replace("]", "").replace("u'", "").replace("[", "").replace("\\r","").replace("'","")
        # **************************************** Eigrp validation initiation ********************************************
                        
                        # ******************************************** BGP Validation **********************************************************
        bgp_filter = ["idle"]
        for state in bgp_filter:
                if bool(re.search(state, bgp_status.decode("utf-8"))) is True:
                        exit.append("BGP is down on ", ip)
                        
                        # *************************************************************************************************************
        tun_int = re.findall('interface (.+?)\n',sec_cmd1.decode('utf-8'))  # to initiate outside interface finding process
        # print(tun_int,type(tun_int),len(tun_int))
        # print(sec_cmd1.decode('utf-8'))
        # *****************************************8888 Finf outside interface ************************************************
        # print(bgp_config,len(bgp_config))
        wan_interfaces = []
        vrf_name_find = ""
        wan_int_split = pre_test_int_status.decode("utf-8").split()
        wan_filte = ["GigabitEthernet", "FastEthernet", "Vlan", "vlan", "Gi", "Ser", "Tunnel"]
        for wi in wan_int_split:
                for si in wan_filte:
                        if bool(re.search(si, wi)) is True and bool(re.search(wi, str(wan_interfaces))) is not True:
                                wan_interfaces.append(wi)
        #print("wan_interfaces", wan_interfaces)
	wan = "False"
        if bool(re.search('send-community', bgp_config.decode("utf-8"))) is True and wan == "True":
                community_line = re.findall('neighbor (.+?) send-community', bgp_config.decode("utf-8"))
                #		print("community_line",community_line)
                nei_ip = re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.', str(community_line)).group()
                print("nei_ip",nei_ip,type(nei_ip),len(nei_ip))
                for wan_int in wan_interfaces:
			print("wan_int",wan_int)
                        tel.write(("show run interface " + wan_int + "\r").encode('ascii'))
			time.sleep(1)
                        wan_int_out = tel.read_until("#".encode('ascii'))
			time.sleep(1)
			#print("************************",wan_int_out+"************************************************8")
                        if bool(re.search(nei_ip, wan_int_out.decode('utf-8'))) is True:
                                interface = wan_int
                                #                               print("wan inter enter")
		#pass
        elif wan=="True":
                tunnels = ["Tunnel40443", "Tunnel17127"]
                print("tunnel zone")
                for tunel in tunnels:
                        tel.write(("sh run int " + tunel + "\r").encode('ascii'))
                        tunel_out = tel.read_until("#".encode('ascii'))
                        #print("tunel",tunel)
                        #print("tunel_out pre",tunel_out)
                        # tel.read_until("#".encode('ascii'))
                        if bool(re.search('% Invalid input detected at', tunel_out.decode("utf-8"))) is not True:
                                interface = tunel
                                #print("tunel_out",tunel_out)
                                #print("interface",interface)
                                # vrf_name_find = re.findall('tunnel vrf (.+?)\n',tunel_out.decode("utf-8"))
                                # print("vrf_name_find",vrf_name_find)
                        
        tun_int = re.findall('interface (.+?)\n', sec_cmd1.decode('utf-8'))
        #print("interface", interface,len(interface),type(interface))
	#print("tun_int",tun_int,len(tun_int),type(tun_int))
        # print(vrf_ouput)
        # vrf_split = vrf_ouput.decode("utf-8").splitlines()
        # print(vrf_split,len(vrf_split),type(vrf_split))
        nat_subnets = ""
        err_status = "True"
        if len(tun_int) > 1:
                exit.append("More than one outside interface found on: " + ip)
                err_status = "false"
                        
        if len(interface) == 0:
                if len(tun_int) == 0:  # to find the interface to shut
                        tel.write("Sh route-map NAT-TO-ADP\r".encode('ascii'))
                        sec_cmd2 = tel.read_until("#".encode('ascii'))
                        tun_int = re.findall('interface (.+?)\n', sec_cmd2.decode('utf-8'))
                        tel.write("Show ip access-list NAT-TO-ADP\r".encode('ascii'))
                        nat_acl = tel.read_until("#".encode('ascii'))
                                        #       print(tun_int,type(tun_int),len(tun_int))
                        if len(tun_int) == 0:  # adp tunnel interface
                                exit.append("NAT-TO CDK and NAT-TO-ADP is not available")
                        elif len(tun_int) == 0:
                                tel.write("Show ip access-list NAT-TO-CDK\r".encode('ascii'))
                                nat_acl = tel.read_until("#".encode('ascii'))
                                nat_subnets = re.findall('permit ip (.+?)\n', nat_acl.decode('utf-8'))
		interface = str(tun_int).replace("[", '').replace("]", '').replace("u'", '').replace("\\r",'').replace("'","").replace('"', '')  # outside interface
                #print("interface",interface)  
                        
                        
                        # ************************************************** Find out LAN interfaces ************************************
        
        filte = ["GigabitEthernet", "FastEthernet", "Vlan", "vlan", "Gi"]
        filtter = ["show", "EIGRP-IPv4", "Xmit", "Interface", "NV0", hostname + "#"]
        eig_chk = "false"
        int_chkk = "false"
        
        int_sli = pre_test_int_status.decode("utf-8").split()
        for spi in int_sli:
                for fi in filte:
                        if bool(re.search(fi, spi)) is True and bool(re.search(spi, str(lan_interfaces))) is not True:
                                lan_interfaces.append(spi)
        #print("lan_interfaces", lan_interfaces)
        if len(lan_interfaces) != 0:
                int_chkk = "True"
                # print("interfaces",vlan_interfaces,type(vlan_interfaces),len(vlan_interfaces))
                for inter in lan_interfaces:
                        tel.write(("show run interface " + inter + "\r\r").encode('ascii'))
			#tel.read_until("#".encode('ascii'))
			if len(lan_interfaces) > 2:
				tel.read_until("#".encode('ascii'))
				#tel.read_until("#".encode('ascii'))
                        	int_out = tel.read_until("#".encode('ascii'))
			else:
				int_out = tel.read_until("#".encode('ascii'))
			#tel.read_until("#".encode('ascii'))
                        int_subnet = re.findall('ip address (.+?)\n', int_out.decode('utf-8'))
                        #print("int out", int_out)
                        if bool(re.search('ip inspect firewall', int_out.decode('utf-8'))) is True:
                                extra_interface.append(inter)
                        elif bool(re.search('zone-member security OUTSIDE', int_out.decode('utf-8'))) is True:
                                extra_interface.append(inter)
                        elif bool(re.search('ip nat outside', int_out.decode('utf-8'))) is True:
                                extra_interface.append(inter)
                        else:
                                # if len(fstvlanint) == 0 or len(primary_interface) == 0:
                                if index == 0:
                                        vlan_interfaces.append(inter)
                                # elif len(fstvlanint) != 0 or len(primary_interface) != 0:
                                elif index == 1:
                                        temp_array.append(
                                                inter)  # temp_array is to catch the second entered ip's details
                                        # print("interfaces gen",vlan_interfaces,type(vlan_interfaces),len(vlan_interfaces))
                                        # print("temp array",temp_array)
        else:
                print("Source interfaces not found on: ", ip)
                fp = os.path.join(save_file_path) + "log.txt"
                with open(fp, "a") as file:
                        file.write("Source interfaces not found on: " + ip)
                        file.close()
                exit.append("Source interfaces not found on: " + ip)
        
        # interface = str(interface_uni )
        # print("interface:",interface,type(interface),len(interface))
        if bool(re.search(interface + " ", down_interface.decode("utf-8"))) is True and err_status != "false":  # to check if the interface is active
                exit.append("interface "+interface + " is down on " + ip)
        
        # *********************************************identify the vrf status and name *********************************************
        vrf_status = "False"
        vrf_name = ""
        eigrp_interface = interface.replace("nnel", "")
	#print("eigrp_interface",eigrp_interface)
        if bool(re.search('unnel', interface)) is True and err_status != "false":  # verify if the interface is tunnel
                
                # print("eigrp int",eigrp_interface)
                #print( tel.read_until("#".encode('ascii'))) 
                #print("askjdKAUGYDyug	q")
                tel.write(("sh run int " + interface + "\r").encode('ascii'))  # to find the primary and secondary router ip
		if len(vlan_interfaces) >3:
			#tel.read_until("#".encode('ascii'))
			#tel.read_until("#".encode('ascii'))
			tun_conf = tel.read_until("#".encode('ascii'))
		else:
			tun_conf = tel.read_until("#".encode('ascii'))
		#time.sleep(1.2)
                #print("tunconfyyy",tun_conf)
		vrf_name_find = re.findall('tunnel vrf (.+?)\n', tun_conf.decode("utf-8"))
                if vrf_name_find:
                        vrf_status = "True"
                        vrf_name = str(vrf_name_find)[2:].replace("'", "").replace("]", "").replace("\\r", "")
                        act_vrf_name.append(vrf_name)
                        #print("vrf_namefind", vrf_name_find)
                # print("tun_conf",tun_conf )
                
                tel.write(("sh ip eigrp vrf " + vrf_name + " nei\r").encode('ascii'))  # to find the primary and secondary router ip
                eigrp_status_vrf = tel.read_until("#".encode('ascii'))
                #print(eigrp_status_vrf) 
                if bool(re.search(eigrp_interface, eigrp_status.decode("utf-8"))) is not True and vrf_status != "True":
                        exit.append("Eigrp is down on " + ip)
                        #print("eigrp_status",eigrp_status)
			#print("interface.replac",interface)
                        #print("eigrp_interface",eigrp_interface)
                elif bool(re.search(eigrp_interface, eigrp_status_vrf.decode("utf-8"))) is not True and vrf_status == "True":
                        exit.append("VRF Eigrp is down on " + ip)
			#print("eigrp_interface",eigrp_interface)
			#print("eigrp_status_vrf",eigrp_status_vrf)
                else:
                        print("")
                
                delay_find = re.findall('delay (.+?)\n', tun_conf.decode('utf-8'))
                delay = str(delay_find).replace("[", '').replace("]", '').replace("u'", '').replace("\\r", '').replace("'", "").replace('"', '')
                # print("first delay",first_delay,type(first_delay),len(first_delay ))
                if len(fstvlanint) == 0:
                        fstip.append(ip)
                	first_delay.append(delay)
               		fstint.append(interface)
                	fstvlanint.append(vlan_interfaces)
                # temp_array.append(fstvlanint)
                	first_delay_str = str(first_delay).replace("[", "").replace("]", "").replace("'", "")
                	second_delay_str = ""
                	fstvrfaware.append(vrf_status)
                # print("fstvlanint first delay",fstvlanint)
                # print("first delay",first_delay)
                else:
                	secip.append(ip)
                	second_delay.append(delay)
                	secint.append(interface)
                	secvlanint.append(temp_array)
                	secvrfaware.append(vrf_status)
                # print("second delay",second_delay,len(second_delay))
                # print("first delay",first_delay)
                	second_delay_str = str(second_delay).replace("[", "").replace("]", "").replace("'", "")
                # print("secvlanint",secvlanint)
                if second_delay:
                # print("second_delay and not primary_ip pimary ip",primary_ip)
                	if str(first_delay).replace("[", "").replace("]", "").replace("'", "") < str(second_delay).replace("[","").replace("]", "").replace("'", ""):
                # print("primary")
                		temp_ip.append(str(fstip).replace("[", "").replace("]", "").replace("u", "").replace('"', ''))
                		primary_interface.append(str(fstint).replace("[", "").replace("]", "").replace("'", ""))
                		primary_vlan_interfaces[:] = []
                		primary_vlan_interfaces.append(fstvlanint)
                		primary_vrf_aware.append(fstvrfaware)
                # print("fstvlanint",fstvlanint)
                	elif str(second_delay).replace("[", "").replace("]", "").replace("'", "") < str(first_delay).replace("[", "").replace("]", "").replace("'", ""):
                # print("secondary")
                		temp_ip.append(str(secip).replace("[", "").replace("]", "").replace('"', '').replace("u",""))  # temp_ip refers to the second entered ip in the UI
               			primary_interface.append(str(secint).replace("[", "").replace("]", "").replace("'", ""))
                		primary_vlan_interfaces[:] = []
                		primary_vlan_interfaces.append(secvlanint)
                		primary_vrf_aware.append(secvrfaware)
                	else:
                		print("both the delay are same")
                		exit.append("both the delay are same")
                
                
	else:
                temp_ip[:] = []
                primary_interface[:] = []
                primary_vlan_interfaces[:] = []
                primary_vrf_aware[:] = []
                temp_ip.append(ip)
                primary_interface.append(interface)
                primary_vlan_interfaces.append(vlan_interfaces)
                primary_vrf_aware.append(vrf_status)
        ip_list = [str(fstip).replace("[", "").replace("]", "").replace("'", "").replace("u", ""),
                           str(secip).replace("[", "").replace("]", "").replace("'", "").replace("u", "")]
                # print("ip list",ip_list)
                
                
	if len(temp_ip) != 0:
        	for ipf in ip_list:
                	if bool(re.search(ipf, str(temp_ip))) is not True:
                        	temp_ip.append(ipf)
                
                # print("temp ip",temp_ip,len(temp_ipif len(temp_ip) == 2:
	if len(temp_ip) == 2:
        	primary_ip.append(temp_ip[0])
                secondary_ip.append(temp_ip[1])
        elif second_delay and len(temp_ip) != 2:
                exit.append("primary or secondary ip not found")
                
     	server_ip_find = re.findall("ip host (.+?)\n", server_ip_result.decode('utf-8'))
                # print(server_ip_find,type(server_ip_find))
        for ser in server_ip_find:
        	s = re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', ser).group()
                server_ip.append(s)
        print("pre test started on: ", ip)
        fp = os.path.join(save_file_path) + "log.txt"
        with open(fp, "a") as file:
        	file.write("pre test started on: " + ip + '\n')
                file.close()
     	fp = os.path.join(save_file_path, ip) + "_pretest" + '_' + '.txt'
        with open(fp, "a") as file:
                file.write('\n' + pre_test_int_status.decode('utf-8'))
               	file.close()
       # print("vlan interface",vlan_interfaces,len(vlan_interfaces))
       # print("temp array",temp_array,len(temp_array))
       # print("server ip ",server_ip,len(server_ip))
                
                
        #print("vrf status", vrf_status)
        #print("vlan_interfaces", vlan_interfaces, len(vlan_interfaces))
                # print("temp_array",temp_array,len(temp_array))
                # print(interface.replace("nnel",""))
                
                
        if (len(vlan_interfaces) != 0 and len(server_ip) != 0):
        	for test_ip in server_ip:
                	# print("test ip ",test_ip)
                	if len(vlan_interfaces) != 0 and len(temp_array) == 0:
                		# print("first")
                        	for test_interface in vlan_interfaces:
                			if vrf_status == "True":
                        			print("first")
               					 # for test_interface in vlan_interfaces:
                
                				tel.write(("telnet " + test_ip + " 80 /vrf " + vrf_name + " /source-interface " + test_interface + "\r").encode('ascii'))
                
                				pre_test_result = tel.read_until("Open".encode('ascii'), 2)
                				print(pre_test_result)
                				# print(out)
                				fp = os.path.join(save_file_path, ip) + "_pretest" + '_' + '.txt'
                                                with open(fp, "a") as file:
                                                        file.write('\n' + pre_test_result.decode('utf-8'))
                                                        file.close()
                                                if bool(re.search('Open', pre_test_result.decode('utf-8'))) is True:
                                                        tel.write('get\r'.encode('ascii'))
                                                        tel.read_until("foreign host]".encode('ascii'), 2)
                                                        tel.read_until("#".encode('ascii'))
                                                        # print(pre_test_result.decode('utf-8'))
                                                        fp = os.path.join(save_file_path) + "log.txt"
                                                        with open(fp, "a") as file:
                                                                file.write('\n' + pre_test_result.decode('utf-8'))
                                                                file.close()
                                                        pre_result_chk.append("Success")  # this will help to identify whether any of the telnet connectivity is success. its used at if not exti section
                                                        success_server.append(test_ip)
                                                        success_interfaces.append(test_interface)
                                                else:
                                                        tel.read_until("#".encode('ascii'))
                                                        # print(pre_test_result.decode('utf-8'))
                                                        fp = os.path.join(save_file_path) + "log.txt"
                                                        with open(fp, "a") as file:
                                                                file.write('\n' + pre_test_result.decode('utf-8'))
                                                                file.close()
                                                        pre_result_chk.append("fail")
                                                        failed_interfaces.append(test_interface)
                                                        # exit.append("DMSCON")
                                                        # exit.append("DMS connectivity issue")
                                                        print("")
                                        else:
                
                                                # for test_interface in vlan_interfaces:
                                                print("fst second")
                                                tel.write(("telnet " + test_ip + " 80 /source-interface " + test_interface + "\r").encode('ascii'))
                
                                                pre_test_result = tel.read_until("Open".encode('ascii'), 2)
                                                print(pre_test_result.decode('utf-8'))
                                                fp = os.path.join(save_file_path, ip) + "_pretest" + '_' + '.txt'
                                                with open(fp, "a") as file:
                                                        file.write('\n' + pre_test_result.decode('utf-8'))
                                                        file.close()
                                                if bool(re.search('Open', pre_test_result.decode('utf-8'))) is True:
                                                        tel.write('get\r\r'.encode('ascii'))
                                                        tel.read_until("foreign host]".encode('ascii'), 2)
                                                        tel.read_until("#".encode('ascii'))
                                                        # print(pre_test_result.decode('utf-8'))
                                                        fp = os.path.join(save_file_path) + "log.txt"
                                                        with open(fp, "a") as file:
                                                                file.write('\n' + pre_test_result.decode('utf-8'))
                                                                file.close()
                                                        pre_result_chk.append("Success")  # this will help to identify whether any of the telnet connectivity is success. its used at if not exti section
                                                        success_server.append(test_ip)
                                                        success_interfaces.append(test_interface)
                                                else:
                                                        tel.read_until("#".encode('ascii'))
                                                        # print(pre_test_result.decode('utf-8'))
                                                        fp = os.path.join(save_file_path) + "log.txt"
                                                        with open(fp, "a") as file:
                                                                file.write('\n' + pre_test_result.decode('utf-8'))
                                                                file.close()
                                                        pre_result_chk.append("fail")
                                                        failed_interfaces.append(test_interface)
                                                        # exit.append("DMSCON")
                                                        # exit.append("DMS connectivity issue")
                                                        print("")
                
                        elif len(temp_array) != 0:
                                print("second")
                                # if vrf_status == "True":
                
                                for test_interface in temp_array:
                                        if vrf_status == "True":
                                        # print("test_interface ",test_interface)
                                                tel.write(("telnet " + test_ip + " 80 /vrf " + vrf_name + " /source-interface " + test_interface + "\r").encode('ascii'))
                
                                                pre_test_result = tel.read_until("Open".encode('ascii'), 2)
                                                print(pre_test_result)
                                                fp = os.path.join(save_file_path, ip) + "_pretest" + '_' + '.txt'
                                                with open(fp, "a") as file:
                                                        file.write('\n' + pre_test_result.decode('utf-8'))
                                                        file.close()
                                                if bool(re.search('Open', pre_test_result.decode('utf-8'))) is True:
                                                        tel.write('get\r'.encode('ascii'))
                                                        tel.read_until("foreign host]".encode('ascii'), 2)
                                                        pre_test_result =  tel.read_until("#".encode('ascii'))
                                                        print(pre_test_result.decode('utf-8'))
                                                        fp = os.path.join(save_file_path) + "log.txt"
                                                        with open(fp, "a") as file:
                                                                file.write('\n' + pre_test_result.decode('utf-8'))
                                                                file.close()
                                                        pre_result_chk.append("Success")  # this will help to identify whether any of the telnet connectivity is success. its used at if not exti section
                                                        success_server.append(test_ip)
                                                        success_interfaces.append(test_interface)
							continue
                                                else:
                                                        tel.read_until("#".encode('ascii'))
							tel.read_until("#".encode('ascii'),2)
                                                        print(pre_test_result.decode('utf-8'))
                                                        fp = os.path.join(save_file_path) + "log.txt"
                                                        with open(fp, "a") as file:
                                                                file.write('\n' + pre_test_result.decode('utf-8'))
                                                                file.close()
                                                        pre_result_chk.append("fail")
                                                        failed_interfaces.append(test_interface)
							continue
                                        if vrf_status == "False":
                                                # for test_interface in temp_array:
                                                # print("server ip",test_ip)
                                                # print("test_interface ",test_interface)
                                                # print("second second")
                                                tel.write(("telnet " + test_ip + " 80 /source-interface " + test_interface + "\r").encode('ascii'))
                
                                                pre_test_result = tel.read_until("Open".encode('ascii'), 2)
                                                print(pre_test_result)
                                                fp = os.path.join(save_file_path, ip) + "_pretest" + '_' + '.txt'
                                                with open(fp, "a") as file:
                                                        file.write('\n' + pre_test_result.decode('utf-8'))
                                                        file.close()
                                                if bool(re.search('Open', pre_test_result.decode('utf-8'))) is True:
                                                        tel.write('get\r\r'.encode('ascii'))
                                                        tel.read_until("foreign host]".encode('ascii'), 2)
                                                        tel.read_until("#".encode('ascii'))
                                                        # print(pre_test_result.decode('utf-8'))
                                                        fp = os.path.join(save_file_path) + "log.txt"
                                                        with open(fp, "a") as file:
                                                                file.write('\n' + pre_test_result.decode('utf-8'))
                                                                file.close()
                                                pre_result_chk.append("Success")  # this will help to identify whether any of the telnet connectivity is success. its used at if not exti section
                                                success_server.append(test_ip)
                                                success_interfaces.append(test_interface)
                                        else:
                                                tel.read_until("#".encode('ascii'))
                                                # print(pre_test_result.decode('utf-8'))
                                                fp = os.path.join(save_file_path) + "log.txt"
                                                with open(fp, "a") as file:
                                                        file.write('\n' + pre_test_result.decode('utf-8'))
                                                        file.close()
                                                pre_result_chk.append("fail")
                                                failed_interfaces.append(test_interface)
                                                print("")
                
                        else:
                                exit.append("Source interface and server ip not found")
                                print("success_server", success_server)
                                pre_result_chk_str = str(pre_result_chk)
                tel.write("sh run\r".encode('ascii'))
                tel.write("sh ip eigrp nei\r".encode('ascii'))
                tel.write("sh ip int brief\r".encode('ascii'))
                tel.write("sh ip bgp summary\r".encode('ascii'))
                tel.write("sh vrf\r".encode('ascii'))
                tel.write("show version\r".encode('ascii'))
                tel.write("wr\r".encode('ascii'))
                tel.write("exit\r".encode('ascii'))
                backup = tel.read_all()
                #	print(backup.decode("utf-8"))
                # *************************8 writing the output to notepad  ***************************************************
                fp = os.path.join(save_file_path, ip) + "_backup" + '.txt'
                with open(fp, "a") as file:
                        file.write(backup.decode('utf-8'))
                        file.close()
                print("backup done on: ", ip)
                fp = os.path.join(save_file_path) + "log.txt"
                with open(fp, "a") as file:
                        file.write('\n' + "configuration backup done on: " + ip + '\n')
                        file.close()


def actual_test():
        shut_interface = str(primary_interface).replace("[", "").replace("]", "").replace("'", "")[1:]
        shut_interface_str = str(shut_interface).strip()
        # print("shut_interface",shut_interface_str,type(shut_interface_str),len(shut_interface_str))
        if bool(re.search('uTun', shut_interface)) is True:
                shut_interface = str(primary_interface).replace("[", "").replace("]", "").replace("'", "")[2:]
        # print("joined")
        
        for serv in success_server:
                if bool(re.search(serv, serv)) is True and bool(re.search(serv, str(actual_server))) is not True:
                        actual_server.append(serv)
        
        # print("active_server",actual_server)
        # print("primary vlan",primary_vlan_interfaces,type(primary_vlan_interfaces),len(primary_vlan_interfaces))
        # print("login ip",ip,type(ip),len(ip))
        # print("primary ip",primary_ip,type(primary_ip),len(primary_ip))
        # print("primary ip",secondary_ip,type(secondary_ip),len(secondary_ip))
        print("shutting the interface", shut_interface + " on " + primary_login_ip)
        tel.write(("ter len 0\r").encode('ascii'))
        tel.read_until("#".encode('ascii'))
        tel.write(("wr\r").encode('ascii'))
        tel.read_until("#".encode('ascii'))
        tel.write(("reload in 10\r").encode('ascii'))
        tel.read_until("[confirm]".encode('ascii'))
        tel.write(("\r").encode('ascii'))
        tel.read_until("#".encode('ascii'))
        tel.write(("conf t \r").encode('ascii'))
        tel.read_until("#".encode('ascii'))
        tel.write(("interface "+shut_interface+"\r").encode('ascii'))
        tel.read_until("#".encode('ascii'))
        tel.write(("shut\r").encode('ascii'))   # to shut the interface
        tel.read_until("#".encode('ascii'))
        tel.write(("end\r").encode('ascii'))
        tel.read_until("#".encode('ascii'))
        fp = os.path.join(save_file_path) + "log.txt"
        with open(fp, "a") as file:
                file.write("reload in 10 activated \n")
                file.write("Interface " + shut_interface + " has been shutdown \n")
                file.write("wait 60 seconds for the traffic to failover\n")
                file.close()
        tel.write(("show ip interface brief | exc unassigned\r").encode('ascii'))
        shut_int_status = tel.read_until("#".encode('ascii'))
        tel.write(("show ip bgp summary\r").encode('ascii'))
        bgp_status = tel.read_until("#".encode('ascii'))
        fp = os.path.join(save_file_path, "actual_test") + '.txt'
        with open(fp, "a") as file:
                file.write('\n'.join([shut_int_status.decode("utf-8"), bgp_status.decode("utf-8")]))
                file.close()
        time.sleep(60)
        clean_primary_vlan_interfaces = str(primary_vlan_interfaces).replace("[", "").replace("]", "").replace("'",
                                                                                                               "").replace(
                "\\r", "").replace("u", "").replace('"', '').split(",")
        print("clean_primary_vlan_interfaces ", clean_primary_vlan_interfaces)
        print("actual test started on: ", primary_login_ip)
        fp = os.path.join(save_file_path) + "log.txt"
        with open(fp, "a") as file:
                file.write("actual test started on: " + primary_login_ip + '\n')
                file.close()
        for test_server_ip in actual_server:
                tel.write(("show ip route " + test_server_ip + "\r").encode('ascii'))
                route_result = tel.read_until("#".encode('ascii'))
                print("route captured")
                fp = os.path.join(save_file_path, "actual_test") + '.txt'
                with open(fp, "a") as file:
                        file.write('\n' + route_result.decode('utf-8'))
                        file.close()
                print("route result copied to notepad")
                # print("test server ip",test_server_ip)
                for test_vlan_interface in clean_primary_vlan_interfaces:
                        # print("test vlan interface",test_vlan_interface,type(test_vlan_interface))
                        
                        tel.write(("telnet " + str(test_server_ip) + " 80 /source-interface " + str(test_vlan_interface) + "\r").encode('ascii'))
                        actual_test_result = tel.read_until("Open".encode('ascii'), 2)
                        # print(out)
                        fp = os.path.join(save_file_path, "actual_test") + '.txt'
                        with open(fp, "a") as file:
                                file.write('\n' + actual_test_result.decode('utf-8'))
                                file.close()
                        if bool(re.search('Open', actual_test_result.decode('utf-8'))) is True:
                                tel.write('get\r'.encode('ascii'))
                                tel.read_until("foreign host]".encode('ascii'), 2)
                                tel.read_until("#".encode('ascii'))
                                print(actual_test_result.decode('utf-8'))
                                fp = os.path.join(save_file_path) + "log.txt"
                                with open(fp, "a") as file:
                                        file.write('\n' + actual_test_result.decode('utf-8'))
                                        file.close()
                                actual_result_chk.append("Success")
                        else:
                                tel.read_until("#".encode('ascii'))
                                print(actual_test_result.decode('utf-8'))
                                fp = os.path.join(save_file_path) + "log.txt"
                                with open(fp, "a") as file:
                                        file.write('\n' + actual_test_result.decode('utf-8'))
                                        file.close()
                                actual_result_chk.append("fail")
                                continue
        fp = os.path.join(save_file_path, "actual_test") + '.txt'
        with open(fp, "a") as file:
                file.write('\n' + shut_int_status.decode("utf-8"))
                file.close()
        tel.write(("conf t \r").encode('ascii'))
        tel.read_until("#".encode('ascii'))
        tel.write(("interface "+shut_interface+"\r").encode('ascii'))
        tel.read_until("#".encode('ascii'))
        tel.write((" no shut\r").encode('ascii'))
        tel.read_until("#".encode('ascii'))
        tel.write(("end\r").encode('ascii'))
        tel.read_until("#".encode('ascii'))
        tel.write(("wr\r").encode('ascii'))
        tel.read_until("#".encode('ascii'))
        fp = os.path.join(save_file_path) + "log.txt"
        with open(fp, "a") as file:
                file.write("Interface " + shut_interface + " has been unshut \n")
                file.write("wait 60 seconds for the traffic to failover\n")
                file.close()
        time.sleep(100)
        tel.write(("show ip interface brief | exc unassigned\r").encode('ascii'))
        enab_int_status = tel.read_until("#".encode('ascii'))
        for test_server_ip in server_ip:
                tel.write(("show ip route " + test_server_ip + "\r").encode('ascii'))
                post_route_status = tel.read_until("#".encode('ascii'))
                fp = os.path.join(save_file_path, "post_test") + '.txt'
                with open(fp, "a") as file:
                        file.write('\n'.join([enab_int_status.decode("utf-8"), post_route_status.decode('utf-8')]))
                        file.close()
        tel.write(("show ip interface brief | exc unassigned\r").encode('ascii'))
        enab_int_status = tel.read_until("#".encode('ascii'))
        tel.write(("show ip bgp summary\r").encode('ascii'))
        enab_bgp_status = tel.read_until("#".encode('ascii'))
        tel.write(("reload cancel\r").encode('ascii'))
        reload_status = tel.read_until("#".encode('ascii'))
        fp = os.path.join(save_file_path, "post_test") + '.txt'
        with open(fp, "a") as file:
                file.write('\n'.join([enab_bgp_status.decode("utf-8"), reload_status]))
                file.close()
        fp = os.path.join(save_file_path) + "log.txt"
        with open(fp, "a") as file:
                file.write("reload cancel done \n")
                file.close()


####################### Execution begins here ####################################
# time.sleep(30)
login_ip = [ip1, ip2]
for index, ip in enumerate(login_ip):
        if isUp(ip) == True:
                tel = telnetlib.Telnet(ip)
                status = "validation"
                if auto_router_login(status) == True:
                        print("")
                else:
                        exit.append("authentication issue on " + ip)
                        #fp = '/var/www/html/failovertests/unauthentic.txt'
                        #with open(fp, "a") as file:
                        #        file.write('\n' + str(ip))
                        #        file.close()
                        fp = os.path.join(save_file_path) + "log.txt"
                        with open(fp, "a") as file:
                                file.write("authentication issue on " + ip + "\n")
                                file.close()
                        continue
                        # tel = telnetlib.Telnet(ip)
                        # manual_router_login(status)
        else:
                print("ip is not reachable")
                fp = os.path.join(save_file_path) + "log.txt"
                with open(fp, "a") as file:
                        file.write(ip, ' is down!' + '\n')
                        file.close()
                exit.append(ip, ' is down!' + '\n')
# print("exit",exit,len(exit))
if bool(re.search("Success", str(pre_result_chk))) is True:
        pre_test_resss = "True"
        pre_test_display = "Atleast one telnet connectivity was suceess during pre test"
        
        # print("pre_test_result",pre_test_result)
else:
        pre_test_display = "None of the telnet connectivity was suceess during pre test"

if not exit and pre_test_resss == "True":
        print("proceeding with post test")
        # print("entered to exit")
        fp = os.path.join(save_file_path) + "log.txt"
        with open(fp, "a") as file:
                file.write('post test started \n')
                file.close()
        print("pri and sec ip", primary_ip, secondary_ip)
        status = "posttest"
        primary_login_ip = str(primary_ip).replace("'", "").replace("[", "").replace("]", "").replace("u", "")
        secondary_login_ip = str(secondary_ip).replace("'", "").replace("[", "").replace("]", "").replace("u", "")
        # print(test_login_ip)
        #	print("primary vlan interfaces",primary_vlan_interfaces)
        ip = secondary_login_ip
        if isUp(ip) == True:
                tel = telnetlib.Telnet(ip)
                if auto_router_login(status) == True:
                        fp = os.path.join(save_file_path) + "log.txt"
                        with open(fp, "a") as file:
                                # file.write("authentication success on "+ip+"\n")
                                file.close()
                else:
                        tel = telnetlib.Telnet(ip)
                        manual_router_login(status)
        else:
                print("ip is not reachable")
                tel.write("ter len 0\r".encode('ascii'))
                tel.read_until("#".encode('ascii'))
        
        #        tel.write(("telnet "+primary_login_ip+"\r").encode('ascii'))
        ip = primary_login_ip
        if isUp(ip) == True:
                tel.write(("telnet " + ip + "\r").encode('ascii'))
                tel_res = tel.read_until("#".encode('ascii'), 2)
                #	print(tel_res)
                if bool(re.search('Open', tel_res.decode("utf-8"))) is not True:
                        print("logging in through VRF " + rvname + "...")
                        fp = os.path.join(save_file_path) + "log.txt"
                        with open(fp, "a") as file:
                                file.write("logging in using VRF please wait for 10 seconds...\n")
                                file.close()
                        rvname = str(act_vrf_name).replace("u", "").replace("'", "").replace("[", "").replace("]", "")
                        tel.write(("telnet " + ip + " /vrf " + rvname + "\r").encode('ascii'))
                
                status = "post_test"
                if auto_router_login(status) == True:
                        print("")
                        fp = os.path.join(save_file_path) + "log.txt"
                        with open(fp, "a") as file:
                                # file.write("authentication success on "+ip+"\n")
                                file.close()
                else:
                        tel.write(("telnet " + ip + "\r").encode('ascii'))
                        manual_router_login(status)
        else:
                print("ip is not reachable")
else:
        print("something went wrong.... possible reasons: ", exit, pre_test_display)
# zip = "cd /var/www/html/failovertests/uploads/; ""tar -zcvf "+new_folder_name+".tar.gz " +new_folder_name+"/"+";"+" mv "+new_folder_name+".tar.gz /var/www/html/failovertests/logs/"" 2> /dev/null"
# os.system(zip)
dir = new_folder_name.replace("/var/www/html/failovertests/uploads/", "")
dir_name = dir + "/"
zip = "cd /var/www/html/failovertests/uploads/; tar -zcvf %s.tar.gz %s; cp %s.tar.gz /var/www/html/failovertests/logs/ 2> /dev/null" % (
        dir, dir_name, dir)
os.system(zip)
save_path = "/var/www/html/failovertests/logs/"
print("File saved path : ", save_path, filename + ".tar.gz")
