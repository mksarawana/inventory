import telnetlib
import string
import os
import csv
import re
import subprocess
import datetime
import time
import sys

now = datetime.datetime.now()
user = "adpnoc"
password = "r0adbl0ck"
#save="/Users/kaliapps/Desktop/My Folder/New folder/failover/Output_files/actual_fo"
a_no=[]
b_yes=[]
crt_ip=[]
interface=[]
reachable_no = []
asp_no =[]
existing = []
not_ping = []
path = sys.argv[1]
username = sys.argv[2]
print(username)
new_folder_name = "/var/www/html/failovertests/uploads/"+username+"_"+datetime.datetime.now().strftime("%m-%d-%y_%H-%M-%S")
if not os.path.exists(new_folder_name):
	os.mkdir(new_folder_name)
save1=new_folder_name+"/"

cmd      = "id "+username
p        = subprocess.Popen(cmd,stdout=subprocess.PIPE, shell=True)
p_status = p.wait()

#if p_status is not 0:
 #   print "Invalid usename"
  #  sys.exit(1)

def restart_program(): # function to Terminate the programme 
    """Restarts the current program.
    Note: this function does not return. Any cleanup action (like
    saving data) must be done before calling this function."""
    python = sys.executable
    os.execl(python, python, * sys.argv)

def get_file_path(filename):
        currentdirpath = os.getcwd()
        file_path = os.path.join(os.getcwd(), filename) # to know the currenr working dir
        return file_path
#path =sys.argv[1]
#path = get_file_path('input.csv')
def read_csv (file_path):
    crt_ip=[]
    interface=[]
    print(file_path)
    with open("/var/www/html/failovertests/uploads/"+file_path, 'r') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)
            for row in reader:
                print("Primary and secondary router IPs :",row)
                pri_log_ip=row[0]
                sec_log_ip=row[1]
                #info = subprocess.STARTUPINFO()
                #info.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                #info.wShowWindow = subprocess.SW_HIDE
                #op = subprocess.Popen(['ping', '-n', '2', '-w', sec_log_ip], stdout=subprocess.PIPE).communicate()[0]
                #if ("64 bytes from " in op.decode('utf-8')):
		response = os.system("ping -c 1 "+pri_log_ip+"> /dev/null")
		if response ==0:
                    print("secondary router "+sec_log_ip+" is reachable")
                    #op = subprocess.Popen(['ping', '-n', '4', '-c', '500', pri_log_ip], stdout=subprocess.PIPE).communicate()[0]
		    #print("printing op",op.decode('utf-8'))
		    response = os.system("ping -c 1 "+pri_log_ip+"> /dev/null")
                    #if ("64 bytes from " in op.decode('utf-8')):
		    if response ==0:
                        print("Primary router "+pri_log_ip+" is reachable")
                        
                    else:
                        not_ping.append(pri_log_ip)
                        print("Not reachable primary router is :",str(not_ping))
                        dp=os.path.join(save1,'primary_Down_sites') + '.txt'
                        with open(dp,"a") as file:
                            file.write('\n'+"Local interfaces not found :"+str(not_ping))
                            print("Not reachable primary router :",pri_log_ip)
                        continue
                else:
                                  
                    not_ping.append(pri_log_ip)
                    print("Not reachable secondary router is :",not_ping)
                    dp=os.path.join(save1,'Secondary_Down_sites') + '.txt'
                    with open(dp,"a") as file:
                        file.write('\n'+"Not reachable secondary router:"+str(not_ping))
                        print("Not reachable secondary router :",sec_log_ip)
                    	continue
                save=save1+pri_log_ip+"_"+datetime.datetime.now().strftime("%m-%d-%y_%H-%M-%S")
                if not os.path.exists(save):
                    os.makedirs(save)
                    
                    tn=telnetlib.Telnet(sec_log_ip)
                    tn.read_until("Username: ".encode('ascii'))
                    tn.write((user + '\r').encode('ascii'))
                    tn.read_until('Password: '.encode('ascii'))
                    tn.write((password + '\r').encode('ascii'))
                    tn.write("en\r".encode('ascii'))
                    tn.read_until('Password: '.encode('ascii'))
                    tn.write(('keep0ut'+ '\r').encode('ascii'))
                    tn.read_until("#".encode('ascii'),2)
                    tn.write(('r0adbl0ck' + '\r').encode('ascii'))
                    tn.write(('n0acce33' + '\r').encode('ascii'))
                    tn.read_until("#".encode('ascii'))
                    print("Logged in to the secondary router",sec_log_ip)
                    tn.write("sh ip int brief | exc unassigned\r".encode('ascii'))
                    tn.read_until("#".encode('ascii'))
                    tn.write("sh run | in asp\r".encode('ascii'))
                    int_det=tn.read_until("#".encode('ascii'))
                    asp_det=tn.read_until("#".encode('ascii')) # to disply sh ip int brief | exc unassigned output to user
                    Err_int=int_det.decode('utf-8')
                    Err_asp=asp_det.decode('utf-8')
                    tn.write("sh vlans dot1q internal\r".encode('ascii'))
                    loo = tn.read_until("#".encode('ascii'))
                    
                    tn.write("show run\r".encode('ascii'))
                    tn.write("sh ip int brief\r".encode('ascii'))
                    tn.write("sh ip eigrp nei\r".encode('ascii'))
                    tn.write("sh cdp nei\r".encode('ascii'))
                    tn.write("exit\r".encode('ascii'))
                    conf=tn.read_all()
                    conf_decode = conf.decode('utf-8')
                    fp = os.path.join(save,sec_log_ip) + '_backup' + '.txt' # To save the back up of show run and etc...
                    
                        
                    with open(fp, "w") as file:
                                
                        file.write(conf_decode)
                        folder = file.write('\n'+"Current time: "+datetime.datetime.now().strftime("%m:%d:%y_%H:%M:%S"))
                    
                        print("Secondary router backup done")
                        
                    ser_lines = Err_asp.replace('ip host aspdms','').replace('ip host aspcrm','').strip('').splitlines()[1:][:-1]
                    ser_ip=[line.split() for line in ser_lines]
                    
                    crt_ip[:]=[]
                    for line in ser_ip:
                            ser_str=str(line)
                            crt_ip.append(ser_str)
                    if crt_ip:
                        pass
                    else:
                        
                        asp_no.append(sec_log_ip)
                        blank_asp = str(asp_no)
                        print(blank_asp)
                        dp=os.path.join(save,'Down_sites') + '.txt'
                        with open(dp,"a") as file:
                            file.write('\n'+" Server IP not found :"+blank_asp)
                            print("Server IP not found on",sec_log_ip)
                        continue
                    #print("crt is:",crt_ip,type(crt_ip),len(crt_ip),len(line))

    ##                lines = Err_asp.splitlines()[2:][:-2]
    ##                m=[line.split() for line in lines]
    ##                interface[:]=[]
    ##                for line in m:
    ##                        int_str=str(line[0])
    ##                        interface.append(int_str)
                            
                    loo_decode = loo.decode('utf-8')
                    loo_split = loo_decode.splitlines()[2:][:-2]
                    loo_str=str(loo_split)
                    loo_space = loo_str.split()
                    rang=len(loo_space)
                    i=0
                    interface[:]=[]
                    while i  < rang:
                        #print(i)
                        i +=5
                        #print("inc i",i)
                        j = i-1
                        #print("j is : ",j)
                        act_int = loo_space[j]
                        act_int_str = str(act_int)
                        inter = act_int_str.replace(")'",'').replace(',','') .replace("'",'').replace(']','')
                        interface.append(inter)           
                    #print(interface)
                    if interface: # Lan interface not found
                            pass
                    else:
                        interface_no.append(sec_log_ip)
                        blank_int = str(interface_no)
                        dp=os.path.join(save,'Down_sites') + '.txt'
                        with open(dp,"a") as file:
                            file.write('\n'+"Local interfaces not found :"+blank_int)
                            print("Local interfaces not found on",sec_log_ip)
                        continue
                    for i in crt_ip:
                        p_ip=i.replace("['",'').replace("']",'').replace("[u'","").replace("'","").replace("[","")
                        print("Testing to server IP :",p_ip)
                        for j in interface:
                            #print(j)
                            tn=telnetlib.Telnet(sec_log_ip)
                            tn.read_until("Username: ".encode('ascii'))
                            tn.write((user + '\r').encode('ascii'))
                            tn.read_until('Password: '.encode('ascii'))
                            tn.write((password + '\r').encode('ascii'))
                            tn.write("en\r".encode('ascii'))
                            tn.read_until('Password: '.encode('ascii'))
                            tn.write(('keep0ut'+ '\r').encode('ascii'))
                            tn.read_until("#".encode('ascii'),2)
                            tn.write(('r0adbl0ck' + '\r').encode('ascii'))
                            tn.write(('n0acce33' + '\r').encode('ascii'))
                            tn.read_until("#".encode('ascii'))
                            #print("Logged in to the secondary router")
                            tn.write("sh ip int brief | exc unassigned\r".encode('ascii'))
                            tn.read_until("#".encode('ascii'))
                            tn.write("sh run | in asp\r".encode('ascii'))
                            int_det=tn.read_until("#".encode('ascii'))
                            asp_det=tn.read_until("#".encode('ascii')) # to disply sh ip int brief | exc unassigned output to user
                            Err_int=int_det.decode('utf-8')
                            Err_asp=asp_det.decode('utf-8')
                            tn.write(("show ip route" +" "+p_ip+"\r").encode('ascii'))
                            tn.write(("telnet " +" "+ p_ip +" "+"80"+" " + "/source-interface"+" "+ j+"\r").encode('ascii'))
                            tn.write('^C\n'.encode('ascii'))
                            tn.write("exit\r".encode('ascii'))
                            list=tn.read_until("Open".encode('ascii'))
                            c=list.decode('utf-8')
                            #print(c)
                            #print("y am i")
                            fp = os.path.join(save,sec_log_ip) + '_cert' + '.txt' # To save the certification results
                            with open(fp, "a") as file:
                                    ##                            
                                    file.write('\n'+c)
                                    file.write('\n'+"Current time: "+datetime.datetime.now().strftime("%m:%d:%y_%H:%M:%S"))
                                    print("Test done from source interface :",j)
                    print("Test done on secondary router")
                    tn=telnetlib.Telnet(pri_log_ip)
                    tn.read_until("Username: ".encode('ascii'))
                    tn.write((user + '\r').encode('ascii'))
                    tn.read_until('Password: '.encode('ascii'))
                    tn.write((password + '\r').encode('ascii'))
                    tn.write("en\r".encode('ascii'))
                    tn.read_until('Password: '.encode('ascii'))
                    tn.write(('keep0ut'+ '\r').encode('ascii'))
                    tn.read_until("#".encode('ascii'),2)
                    tn.write(('r0adbl0ck' + '\r').encode('ascii'))
                    tn.write(('n0acce33' + '\r').encode('ascii'))
                    tn.read_until("#".encode('ascii'))
                    print("Logged in to the primary router",pri_log_ip)
                    tn.write("sh ip int brief | exc unassigned\r".encode('ascii'))
                    tn.read_until("#".encode('ascii'))
                    tn.write("sh run | in asp\r".encode('ascii'))
                    int_det=tn.read_until("#".encode('ascii'))
                    asp_det=tn.read_until("#".encode('ascii')) # to disply sh ip int brief | exc unassigned output to user
                    Err_int=int_det.decode('utf-8')
                    Err_asp=asp_det.decode('utf-8')
                    tn.write("sh vlans dot1q internal\r".encode('ascii'))
                    loo = tn.read_until("#".encode('ascii'))
                    tn.write("show run\r".encode('ascii'))
                    tn.write("sh ip int brief\r".encode('ascii'))
                    tn.write("sh ip eigrp nei\r".encode('ascii'))
                    tn.write("sh cdp nei\r".encode('ascii'))
                    tn.write("exit\r".encode('ascii'))
                    conf=tn.read_all()
                    conf_decode = conf.decode('utf-8')
                    fp = os.path.join(save,pri_log_ip) + '_backup' + '.txt' # To save the back up of show run and etc...
                    with open(fp, "w") as file:
                                            
                            file.write(conf_decode)
                            file.write('\n'+"Current time: "+datetime.datetime.now().strftime("%m:%d:%y_%H:%M:%S"))
                            #print("Primary router backup done")

                    ser_lines = Err_asp.replace('ip host aspdms','').replace('ip host aspcrm','').strip('').splitlines()[1:][:-1]
                    ser_ip=[line.split() for line in ser_lines]
                    crt_ip[:]=[]
                    for line in ser_ip:
                            ser_str=str(line)
                            crt_ip.append(ser_str)
                    if crt_ip:
                        pass
                    else:
                        asp_no.append(pri_log_ip)
                        blank_asp = str(asp_no)
                        dp=os.path.join(save,'Down_sites') + '.txt'
                        with open(dp,"a") as file:
                            file.write('\n'+"Server IP not found on :"+blank_asp)
                            print("Server IP not found on",pri_log_ip)
                        continue
                    #print("crt is:",crt_ip,type(crt_ip),len(crt_ip),len(line))
    ##                lines = Err_asp.splitlines()[2:][:-2]
    ##                m=[line.split() for line in lines]
    ##                interface[:]=[]
    ##                for line in m:
    ##                        int_str=str(line[0])
    ##                        interface.append(int_str)
                    loo_decode = loo.decode('utf-8')
                    loo_split = loo_decode.splitlines()[2:][:-2]
                    loo_str=str(loo_split)
                    loo_space = loo_str.split()
                    rang=len(loo_space)
                    i=0
                    interface[:]=[]
                    while i  < rang:
                        #print(i)
                        i +=5
                        #print("inc i",i)
                        j = i-1
                        #print("j is : ",j)
                        act_int = loo_space[j]
                        act_int_str = str(act_int)
                        inter = act_int_str.replace(")'",'').replace(',','') .replace("'",'').replace(']','')
                        interface.append(inter)           
                    #print(interface)
                    if interface: # Lan interface not found
                            pass
                    else:
                        interface_no.append(pri_log_ip)
                        blank_int = str(interface_no)
                        dp=os.path.join(save,'Down_sites') + '.txt'
                        with open(dp,"a") as file:
                            file.write('\n'+"Local interfaces not found :"+blank_int)
                            print("Local interfaces not found on",pri_log_ip)
                        
                        continue

                    for i in crt_ip:
                        p_ip=i.replace("['",'').replace("']",'').replace("[u'","").replace("'","").replace("[","")
                        print("Testing to server IP :",p_ip)
                        for j in interface:
                            #print(j)
                            tn=telnetlib.Telnet(pri_log_ip)
                            
                            tn.read_until("Username: ".encode('ascii'))
                            tn.write((user + '\r').encode('ascii'))
                            tn.read_until('Password: '.encode('ascii'))
                            tn.write((password + '\r').encode('ascii'))
                            tn.write("en\r".encode('ascii'))
                            tn.read_until('Password: '.encode('ascii'))
                            tn.write(('keep0ut'+ '\r').encode('ascii'))
                            tn.read_until("#".encode('ascii'),2)
                            tn.write(('r0adbl0ck' + '\r').encode('ascii'))
                            tn.write(('n0acce33' + '\r').encode('ascii'))
                            tn.read_until("#".encode('ascii'))
                            #print("Logged in to the primary router")
                            tn.write("sh ip int brief | exc unassigned\r".encode('ascii'))
                            tn.read_until("#".encode('ascii'))
                            tn.write("sh run | in asp\r".encode('ascii'))
                            int_det=tn.read_until("#".encode('ascii'))
                            asp_det=tn.read_until("#".encode('ascii')) # to disply sh ip int brief | exc unassigned output to user
                            Err_int=int_det.decode('utf-8')
                            Err_asp=asp_det.decode('utf-8')
                            tn.write(("show ip route" +" "+p_ip+"\r").encode('ascii'))
                            tn.write(("telnet " +" "+ p_ip +" "+"80"+" " + "/source-interface"+" "+ j+"\r").encode('ascii'))
                                    
                                    #
                            tn.write('^C\n'.encode('ascii'))
                            tn.write("exit\r".encode('ascii'))
                            list=tn.read_until("Open".encode('ascii'))
                            
                               
                                    ##                    
                            c=list.decode('utf-8')
                            #print(c)
                                    #
                            fp = os.path.join(save,pri_log_ip) + '_cert' + '.txt' # To save the certification results
                            with open(fp, "a") as file:
                                    ##                            
                                    file.write('\n'+c)
                                    file.write('\n'+"Current time: "+datetime.datetime.now().strftime("%m:%d:%y_%H:%M:%S"))
                                    print("Test done from source interface :",j)
                                                                                            
                                                    
                    print("Test done on primary router")
                    #print(Err_int) # Showing interface result to users
                    int_status_searchResult=re.search('down',Err_int,re.M|re.I)
                    if int_status_searchResult:
                        desi = int_status_searchResult.group()

                            
                        a_no.append(pri_log_ip)
                        print("IP noted as down is :",a_no)
                        down_list=str(a_no)
                        dp=fp = os.path.join(save,'Down_sites') + '.txt'
                        with open(dp,"a") as file:
                            file.write('\n'+"Interface down issues :"+down_list)
                        continue
                            #break
                    else:        # Login to secondary router to identify the down interface
                        tn=telnetlib.Telnet(sec_log_ip)
                        tn.read_until("Username: ".encode('ascii'))
                        tn.write((user + '\r').encode('ascii'))
                        tn.read_until('Password: '.encode('ascii'))
                        tn.write((password + '\r').encode('ascii'))
                        tn.write("en\r".encode('ascii'))
                        tn.read_until('Password: '.encode('ascii'))
                        tn.write(('keep0ut'+ '\r').encode('ascii'))
                        tn.read_until("#".encode('ascii'),2)
                        tn.write(('r0adbl0ck' + '\r').encode('ascii'))
                        tn.write(('n0acce33' + '\r').encode('ascii'))
                        tn.read_until("#".encode('ascii'))
                        #print("successfully logged in to the secondary router")
                        tn.write('sh ip int brief | exc unassigned\r'.encode('ascii'))
                        tn.read_until("#".encode('ascii'))
                        tn.write('sh run | in asp\r'.encode('ascii'))
                        int_det=tn.read_until("#".encode('ascii'))
                        asp_det=tn.read_until("#".encode('ascii')) # to disply sh ip int brief | exc unassigned output to user
                        Err_int=int_det.decode('utf-8')
                        Err_asp=asp_det.decode('utf-8')
                        int_status_searchResult=re.search('down',Err_int,re.M|re.I)
                        if int_status_searchResult:
                            desi = int_status_searchResult.group()
                            print("Interface down issue found")
                            
                            a_no.append(sec_log_ip)
                            print("IP noted as down :",a_no)
                            down_list=str(a_no)
                            dp = os.path.join(save,'Down_sites') + '.txt'
                            with open(dp,"a") as file:
                                file.write('\n' + "Interface down issues :"+down_list)
                            continue 
                        
    ##                                        
                    

                    # Actual test started here
                    tn=telnetlib.Telnet(pri_log_ip)
                    #print("Logging in to shut the interface on :",pri_log_ip)
                    tn.read_until("Username: ".encode('ascii'))
                    tn.write((user + '\r').encode('ascii'))
                    tn.read_until('Password: '.encode('ascii'))
                    tn.write((password + '\r').encode('ascii'))
                    tn.write("en\r".encode('ascii'))
                    tn.read_until('Password: '.encode('ascii'))
                    tn.write(('keep0ut'+ '\r').encode('ascii'))
                    tn.read_until("#".encode('ascii'),2)
                    tn.write(('r0adbl0ck' + '\r').encode('ascii'))
                    tn.write(('n0acce33' + '\r').encode('ascii'))
                    tn.read_until("#".encode('ascii'))
                    
                    tn.write(("clear configuration lock\r").encode('ascii')) # To clear the configuration lock
                    tn.read_until("]".encode('ascii'),2)
                    tn.write(("y\r").encode('ascii'))
                    tn.read_until("#".encode('ascii'),1)
                    tn.write(('reload in 10\r').encode('ascii')) # Seeting the router to reload in 10 minutes
                    tn.read_until("]".encode('ascii'))
                    tn.write(("y\r").encode('ascii'))
                    tn.read_until("#".encode('ascii'),1)
                    tn.read_until("#".encode('ascii'))
                    print("reload in 10 activated on primary router")
                    tn.write("sh run | in match interface\r".encode('ascii'))
                    tu = tn.read_until("#".encode('ascii'))
                    
    ##                while True:
    ##                        int_name=input("Please enter the name of the interface to shut(Tunnel or SDN):") # Asking the user to enter the interface to shut
    ##                        intResult=re.search(int_name,Err_int,re.M|re.I)
    ##                        if intResult:
    ##                                print("Search Found: "+intResult.group())
    ##                                break
    ##                        else:
    ##                            print("Enter the interface name as same as shows in router")
    ##                #tn.read_until("#".encode('ascii'))
                    tu_decode = tu.decode('utf-8')
                    tu_split = tu_decode.splitlines()[1:]
                    tu_str = str(tu_split)
                    tu_space = tu_str.replace("'",'').replace(',','').split()
                    if tu_space: # Match interface has not configured
                        pass
                    else:
                        tunnel_no.append(pri_log_ip)
                        blank_tunnel = str(tunnel_no)
                        dp=os.path.join(save,'Down_sites') + '.txt'
                        with open(dp,"a") as file:
                            file.write('\n'+" Tunnel interface not found on :"+blank_int)
                            
                        print("Tunnel interface not found on",pri_log_ip)
                        continue
                    #print(tu_space[3],type(tu_space),len(tu_space))
                    int_name = tu_space[3]
                    tn.write(("clear configuration lock\r").encode('ascii'))
                    tn.read_until("]".encode('ascii'),2)
                    tn.write(("y\r").encode('ascii'))
                    tn.read_until("#".encode('ascii'))
                    tn.write(("conf t\r").encode('ascii'))
                    inter_vali=tn.read_until("#".encode('ascii'))
                    #print(inter_vali)
                    tn.write(("interface" +" "+int_name+"\r").encode('ascii'))
                    inva=tn.read_until("#".encode('ascii'))
                    int_validation=inter_vali.decode('utf-8')
                    #print(int_validation)
                    # Validation of interface to make sure user has entered the correct interface
                    invasearchResult=re.search('Connection refused by remote host',int_validation,re.M|re.I)
                    invasearchResult=re.search('Bad IP address',int_validation,re.M|re.I)
                    invasearchResult=re.search('Incomplete command',int_validation,re.M|re.I)
                    invasearchResult=re.search('Invalid input detected',int_validation,re.M|re.I)
                    if invasearchResult: # if the user enters the worng interface program gets terminat
                        print("Search Found: "+invasearchResult.group())
                        print("Please re run the script with correct interface name")
                        tn.write(("reload cancel\r").encode('ascii'))
                        print("reload cancelled")
                        continue
                    else: # if it is right interface, it contiues 
                        tn.write(("shut\r").encode('ascii'))
                        print("Interface "+int_name+" "+"has been shut on primary router")



                # codes for secondary router


                            
                    print("Please wait till we get reachability to secondary router...")
                    time.sleep(60)
                    # Testing the reachability of the secondary router        
                    #info = subprocess.STARTUPINFO()
                    #info.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                    #info.wShowWindow = subprocess.SW_HIDE
                    #op = subprocess.Popen(['ping', '-n', '4', '-w', '500', sec_log_ip], stdout=subprocess.PIPE).communicate()[0]
                    # Loging in to the secondary router
                    #if ("64 bytes from " in op.decode('utf-8')):
		    response = os.system("ping -c 1 "+sec_log_ip+" > /dev/null")
		    if response == 0:
                        print("Logging in to perform test on secondary router:",sec_log_ip)
                        tn=telnetlib.Telnet(sec_log_ip)
                        tn.read_until("Username: ".encode('ascii'))
                        tn.write((user + '\r').encode('ascii'))
                        tn.read_until('Password: '.encode('ascii'))
                        tn.write((password + '\r').encode('ascii'))
                        tn.write("en\r".encode('ascii'))
                        tn.read_until('Password: '.encode('ascii'))
                        tn.write(('keep0ut'+ '\r').encode('ascii'))
                        tn.read_until("#".encode('ascii'),2)
                        tn.write(('r0adbl0ck' + '\r').encode('ascii'))
                        tn.write(('n0acce33' + '\r').encode('ascii'))
                        tn.read_until("#".encode('ascii'))
                        print("successfully logged in to the secondary router")

                        # collecting needed output to display user
                        tn.write('sh ip int brief | exc unassigned\r'.encode('ascii'))
                        tn.read_until("#".encode('ascii'))
                        tn.write('sh run | in asp\r'.encode('ascii'))
                        int_det=tn.read_until("#".encode('ascii'))
                        asp_det=tn.read_until("#".encode('ascii')) # to disply sh ip int brief | exc unassigned output to user
                        Err_int=int_det.decode('utf-8')
                        Err_asp=asp_det.decode('utf-8')
                        tn.write("sh vlans dot1q internal\r".encode('ascii'))
                        loo = tn.read_until("#".encode('ascii'))
                        print(int_det.decode('utf-8'))#display the interface detail
                        print("*****************************************")
                        print(asp_det.decode('utf-8'))# To display sh run | in asp output to user
                        print("*****************************************")
                                    


                                                    # collecting the values from user to test the failover

                        ser_lines = Err_asp.replace('ip host aspdms','').replace('ip host aspcrm','').strip('').splitlines()[1:][:-1]
                        ser_ip=[line.split() for line in ser_lines]
                        crt_ip[:]=[]
                        for line in ser_ip:
                            ser_str=str(line)
                            crt_ip.append(ser_str)
    ##                    while True:
    ##                        try:
    ##                            crt_ip=input("Enter the server IP address seperated by comma without space[,]:").strip().split(',')
    ##                            print(crt_ip,type(crt_ip),len(crt_ip))
    ##                            break
    ##                        except KeyboardInterrupt:
    ##                            print("Enter the value")
    ##                    while True:
    ##                        try:
    ##                            interface=input("Enter the interfaces name seperated by comma without any space[,]:").strip().split(',')
    ##                            #print(interface,type(interface),len(interface))
    ##                            break
    ##                        except KeyboardInterrupt:
    ##                            print("Enter the value")
                        loo_decode = loo.decode('utf-8')
                        loo_split = loo_decode.splitlines()[2:][:-2]
                        loo_str=str(loo_split)
                        loo_space = loo_str.split()
                        #print(loo_space,len(loo_space))
                        rang=len(loo_space)
                        i=0
                        interface[:]=[]
                        while i  < rang:
                            #print(i)
                            i +=5
                            #print("inc i",i)
                            j = i-1
                            #print("j is : ",j)
                            act_int = loo_space[j]
                            act_int_str = str(act_int)
                            inter = act_int_str.replace(")'",'').replace(',','') .replace("'",'').replace(']','')
                            interface.append(inter)           
                        #print(interface)
                        if interface: # Lan interface not found
                            pass
                        else:
                            interface_no.append(sec_log_ip)
                            blank_int = str(interface_no)
                            dp=os.path.join(save,'Down_sites') + '.txt'
                            with open(dp,"a") as file:
                                file.write('\n'+"Unreachable Secondary routers :"+blank_int)
                            print("Local interfaces not found on",sec_log_ip)
                            continue

                        for i in crt_ip:
                            p_ip=i.replace("['",'').replace("']",'').replace("[u'","").replace("'","").replace("[","")
                            print("Testing for ip :",p_ip)
                            for j in interface:
                                     
                                tn=telnetlib.Telnet(sec_log_ip) # Login again to the routes(as per for loop) to perform the tests
                                tn.read_until("Username: ".encode('ascii'))
                                tn.write((user + '\r').encode('ascii'))
                                tn.read_until('Password: '.encode('ascii'))
                                tn.write((password + '\r').encode('ascii'))
                                tn.write("en\r".encode('ascii'))
                                tn.read_until('Password: '.encode('ascii'))
                                tn.write(('keep0ut'+ '\r').encode('ascii'))
                                tn.read_until("#".encode('ascii'),2)
                                tn.write(('r0adbl0ck' + '\r').encode('ascii'))
                                tn.write(('n0acce33' + '\r').encode('ascii'))
                                tn.read_until("#".encode('ascii'))
                                tn.read_until("#".encode('ascii'))
                                #print(type(crt_ip))
                                tn.write(("show ip route" +" "+p_ip+"\r").encode('ascii'))
                                tn.write(("telnet " +" "+ p_ip +" "+"80"+" " + "/source-interface"+" "+ j+"\r").encode('ascii'))
                                                
                                                #
                                tn.write('^C\n'.encode('ascii'))
                                tn.write("exit\r".encode('ascii'))
                                list=tn.read_until("Open".encode('ascii'))
                                
                                                
                                                ##                    
                                c=list.decode('utf-8')
                                #print(c)
                                fp = os.path.join(save,sec_log_ip) + 'post_cert' + '.txt' # To save the certification results
                                with open(fp, "a") as file:
                                                ##                            
                                                file.write('\n'+c)
                                                file.write('\n'+"Current time: "+datetime.datetime.now().strftime("%m:%d:%y_%H:%M:%S"))
                                                print("Test done from source interface :",j)
   
                    else:
                        reachable_no.append(sec_log_ip)
                        not_reach = str(reachable_no)
                        print("Not reachable secondary router is :",sec_log_ip)
                        dp= os.path.join(save,'Down_sites') + '.txt'
                        with open(dp,"a") as file:
                            file.write('\n'+"Unreachable Secondary routers :"+not_reach)
                            
                        #pri_op = subprocess.Popen(['ping', '-n', '4', '-w', '500', pri_log_ip], stdout=subprocess.PIPE).communicate()[0]
                        #if "64 bytes from " in pri_op.decode('utf-8'):
			response = os.system("ping -c 1 "+pri_log_ip+" > /dev/null")
                        if response == 0:

                                        print("primary router is reachable")
                                        tn=telnetlib.Telnet(pri_log_ip)
                                        tn.read_until("Username: ".encode('ascii'))
                                        tn.write((user + '\r').encode('ascii'))
                                        tn.read_until('Password: '.encode('ascii'))
                                        tn.write((password + '\r').encode('ascii'))
                                        tn.write("en\r".encode('ascii'))
                                        tn.read_until('Password: '.encode('ascii'))
                                        tn.write(('keep0ut'+ '\r').encode('ascii'))
                                        tn.read_until("#".encode('ascii'),2)
                                        tn.write(('r0adbl0ck' + '\r').encode('ascii'))
                                        tn.write(('n0acce33' + '\r').encode('ascii'))
                                        tn.read_until("#".encode('ascii'))
                                        print("successfully logged in to the primary router")
                                        tn.write('show run | in hostname\r'.encode('ascii'))
                                        hn=tn.read_until("#".encode('ascii'))
                                        tn.write(("clear configuration lock\r").encode('ascii'))
                                        tn.read_until("#".encode('ascii'))
                                        tn.write(('y\r').encode('ascii'))
                                        tn.read_until("#".encode('ascii'))
                                        tn.write(("conf t\r").encode('ascii'))
                                        tn.read_until("#".encode('ascii'))
                                        tn.write(("interface" +" "+int_name+"\r").encode('ascii'))
                                        tn.read_until("#".encode('ascii'))
                                        tn.write(("no shut\r").encode('ascii'))
                                        print("Interface "+int_name+" "+"has been UNSHUT")
                                        tn.read_until("#".encode('ascii'))
                                        tn.write(("end\r").encode('ascii'))
                                        tn.read_until("#".encode('ascii'))

                                        tn.write(("reload cancel\r").encode('ascii'))
                                        tn.read_until("#".encode('ascii'))
                                        print("Reload canceled")
                                        tn.read_until("#".encode('ascii'))
                                        tn.write(("show ip route" +" "+i+"\r").encode('ascii'))
                                        ro=tn.read_until("#".encode('ascii'))
                                        tn.write(("show ip int brief | exc unassigned\r").encode('ascii'))
                                        tn.write(("show ip route" +" "+i+"\r").encode('ascii'))
                                        #tn.write(("wr\r").encode('ascii'))

                                        io=tn.read_until("#".encode('ascii'))
                                        e=io.decode('utf-8')
                                        f=ro.decode('utf-8')
                                        print(ro.decode('utf-8'))
                                        print(io.decode('utf-8'))
                                        fp = os.path.join(save,pri_log_ip) + '_post_cert' + '.txt' # To save the certification results
                                        with open(fp, "a") as file:
                                                        file.write('\n'+e)
                                                        file.write('\n'+f)
                                                        file.write('\n'+"Currect time: "+datetime.datetime.now().strftime("%m:%d:%y_%H:%M:%S"))
                                                        #print("Currect time: "+datetime.datetime.now().strftime("%m:%d:%y_%H:%M:%S"))
                        else:
                            
                            reachable_no.append(pri_log_ip)
                            print("Not reachable primary router is :",reachable_no)
                            dp = os.path.join(save,'Down_sites') + '.txt'
                            with open(dp,"a") as file:
                                reachable_no_str = str(reachable_no)
                                file.write('\n'+"Unreachable primary routers :"+reachable_no_str)
                            continue
                                                            #Revert back
                    tn=telnetlib.Telnet(pri_log_ip)
                    tn.read_until("Username: ".encode('ascii'))
                    tn.write((user + '\r').encode('ascii'))
                    tn.read_until('Password: '.encode('ascii'))
                    tn.write((password + '\r').encode('ascii'))
                    tn.write("en\r".encode('ascii'))
                    tn.read_until('Password: '.encode('ascii'))
                    tn.write(('keep0ut'+ '\r').encode('ascii'))
                    tn.read_until("#".encode('ascii'),2)
                    tn.write(('r0adbl0ck' + '\r').encode('ascii'))
                    tn.write(('n0acce33' + '\r').encode('ascii'))
                    tn.read_until("#".encode('ascii'))
                    print("successfully logged in to the primary router")
                    tn.write('show run | in hostname\r'.encode('ascii'))
                    hn=tn.read_until("#".encode('ascii'))
                    tn.write(("clear configuration lock\r").encode('ascii'))
                    tn.read_until("#".encode('ascii'))
                    tn.write(('y\r').encode('ascii'))
                    tn.read_until("#".encode('ascii'))
                    tn.write(("conf t\r").encode('ascii'))
                    tn.read_until("#".encode('ascii'))
                    tn.write(("interface" +" "+int_name+"\r").encode('ascii'))
                    tn.read_until("#".encode('ascii'))
                    tn.write(("no shut\r").encode('ascii'))
                    print("Interface "+int_name+" "+"has been UNSHUT")
                    tn.read_until("#".encode('ascii'))
                    tn.write(("end\r").encode('ascii'))
                    tn.read_until("#".encode('ascii'))
                    tn.write(("reload cancel\r").encode('ascii'))
                    tn.read_until("#".encode('ascii'))
                    print("Reload canceled")
                    tn.read_until("#".encode('ascii'))

                    print("Please wait for the route flip back to primary...")
                    time.sleep(100)

                    tn.write(("show ip route" +" "+p_ip+"\r").encode('ascii'))
                    ro=tn.read_until("#".encode('ascii'))
                    tn.write(("show ip int brief | exc unassigned\r").encode('ascii'))
                    #tn.write(("wr\r").encode('ascii'))
                    io=tn.read_until("#".encode('ascii'))
                    e=io.decode('utf-8')
                    f=ro.decode('utf-8')
                    #print(ro.decode('utf-8'))
                    #print(io.decode('utf-8'))
                    fp = os.path.join(save,pri_log_ip) + '_post_cert' + '.txt' # To save the certification results
                    with open(fp, "a") as file:
                        file.write('\n'+e)

                        file.write('\n'+f)
                        file.write('\n'+"Currect time: "+datetime.datetime.now().strftime("%m:%d:%y_%H:%M:%S"))
                        #print("Current time: "+datetime.datetime.now().strftime("%m:%d:%y_%H:%M:%S"))
                else:
				
                    	existing.append(row[0])
                    	print("existing folder "+row[0]+" found")
                    	#continue
		#    	zip = "cd /usr/local/NIS;  tar -zcvf "+pri_log_ip+"tar.gz "+pri_log_ip+"/"+";"+" mv /usr/local/NIS/"+pri_log_ip+"tar.gz "+" /home/sarava/repo"
		 #   	os.system(zip)
		    	#tar_copy = "mv /usr/local/NIS/"+pri_log_ip+"tar.gz "+" /home/sarava/repo"
		    	#os.system(tar_copy)
		  #  	print("ZIP and Tar ",zip
		    	continue

download_path = new_folder_name.replace("uploads","logs")
dir = new_folder_name.replace("/var/www/html/failovertests/uploads/","")
dir_name = dir+"/"
zip = "cd /var/www/html/failovertests/uploads/; tar -zcvf %s.tar.gz %s; cp %s.tar.gz /var/www/html/failovertests/logs/ > /dev/null" %(dir,dir_name,dir)
#zip = "cd /var/www/html/failovertests/uploads/; ""tar -zcvf "+new_folder_name+".tar.gz " +new_folder_name+"/"+";"+" mv "+new_folder_name+".tar.gz /var/www/html/failovertests/logs/;""sudo chmod 777 "+download_path+".tar.gz > /dev/null"
#zip = "cd /var/www/html/failovertests/uploads/; tar -zcvf %s.tar.gz %s; mv %s.tar.gz /var/www/html/failovertests/logs/ > /dev/null"
#zip = "cd /var/www/html/failovertests/uploads/; tar -zcf %s.tar.gz %s 2> /dev/null" %(new_folder_name,new_folder_name)
os.system(zip)
download_path = new_folder_name.replace("uploads","logs")
read_csv(path)
print("Down sites from actual test:",a_no)
#print("Site down IPs saved in to notepad (Down_sites) at:",save)
#print("Activity completed")
print("Existing folders found are :",existing)
print("Activity completed")
print("File saved path : ",download_path+".tar.gz")
#input("Please send your feedback or suggession about this tool to mail id : saravanan.kaliappan@cdk.com")

