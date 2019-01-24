import psutil
import lcddriver
import subprocess
from time import sleep

lcd = lcddriver.Lcd()
lcd.lcd_clear()

##############################################
#  Shows information about PiCluster on LCD  #
# ------------------------------------------ #
# Line 1 : TwoDigits                         #
# Line 2 : Interface + IP                    #
# Line 3 : Mem + CPU Master                  #
# Line 4 : Nodes + (CPU & Mem of Nodes)      #
##############################################

line_pos = [0 , 0 , 0 , 0]
line_data = ["", "", "", ""] 
update_counter = [9999, 9999, 9999, 9999]
# How many cycles should be skipped before the next update?
update_limit = [5, 1000, 10, 100]
cycle_len = 0.25

def update_revport():
    status = ""
    p = subprocess.Popen('/etc/init.d/reverseport status', shell = True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in p.stdout.readlines():
        status = status+"{0}".format(line)[2:-3]
    retval = p.wait()
    return "Reverseport : {0}".format(status)

def update_nodes():
    pods_running = ""
    pods_total = ""
    p = subprocess.Popen('kubectl get pods|grep "Running"|wc -l', shell = True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in p.stdout.readlines():
        pods_running = line
    retval = p.wait()
    p = subprocess.Popen('kubectl get pods|wc -l', shell = True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in p.stdout.readlines():
        pods_total = line
    retval = p.wait()
    return "Pods Running : {0}".format(pods_running) + " Total : {0}".format(pods_total)

def update_ips():
    # configure the interfaces which should be shown in line2
    interfaces = ['wlan0', 'enxb827ebe2c89e']

    ips = ""

    for key in interfaces:
        if key in psutil.net_if_addrs().keys():
            for addr in psutil.net_if_addrs()[key]:
                if addr.family == 2:
                    ips = ips + key + " : " + addr.address + "    "
            if key == 'wlan0':
                p = subprocess.Popen('iwconfig wlan0|grep ESSID|awk \'{print $4;}\'', shell = True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                for line in p.stdout.readlines():
                    ips = ips+"{0}".format(line)[2:-3] + "    "
                retval = p.wait()
    return ips


def update_memory():
    mem_free_master = psutil.virtual_memory().free / 1024 / 1024
    mem_used_master = psutil.virtual_memory().used / 1024 / 1024
    return "Mem Free :{:4.0f} MB ".format(mem_free_master) + " Used : {:4.0f} MB".format(mem_used_master)



def update_display():
    global line_pos
    global line_data
    global update_counter
    global update_limit

    for i in [1 , 2 , 3]:
        update_counter[i]=update_counter[i]+1;
        if update_counter[i] >= update_limit[i]:
            update_counter[i] = 0;
            if i==1:
                line_data[i] = update_ips();
            if i==2:
                line_data[i] = update_memory();
            if i==3:
                line_data[i] = update_revport(); 
    line_data[0] = "     TwoDigits"
    
    for i in [0 , 1 , 2 , 3]:
        line_len = len(line_data[i])
        if line_len <= 20:
            lcd.lcd_display_string(line_data[i], i+1)
        else:
            line = line_data[i] + " " + line_data[i]
            lcd.lcd_display_string(line[line_pos[i]:20+line_pos[i]], i+1)
            line_pos[i] = line_pos[i] + 1
            if line_pos[i] > line_len:
                line_pos[i] = 0


while True:
    update_display();
    sleep(cycle_len);

