import psutil
import lcddriver

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


def update_ips():
    # configure the interfaces which should be shown in line2
    interfaces = ['wlan0', 'enxb827ebe2c89e']

    ips = ""

    for key in interfaces:
        if key in psutil.net_if_addrs().keys():
            for addr in psutil.net_if_addrs()[key]:
                if addr.family == 2:
                    ips = ips + key + " : " + addr.address + "    "
    return ips


def update_memory():
    mem_free_master = psutil.virtual_memory().free / 1024 / 1024
    mem_used_master = psutil.virtual_memory().used / 1024 / 1024
    return "Mem Free : {0}".format(mem_free_master) + " Mem Used : {0}".format(mem_used_master)


# TODO : implement marquee if len is more then 20 chars
def update_display():
    line1 = "     TwoDigits"
    line2 = update_ips()
    line3 = update_memory()
    line4 = "Nodes"  # TODO : implement node info from kubernetes
    lcd.lcd_display_string(line1, 1)
    lcd.lcd_display_string(line2, 2)
    lcd.lcd_display_string(line3, 3)
    lcd.lcd_display_string(line4, 4)


# TODO : do it in a loop with 250ms timeout?
update_display()


