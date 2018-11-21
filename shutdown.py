#! /usr/bin/python3

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



def update_display():
    global line_pos
    #        00000000011111111112
    #        12345678901234567890
    line1 = "     TwoDigits"
    line2 = ""
    line3 = " Shutdown completed "
    line4 = "  Have a nice day!  "  
    
    lines = [line1 , line2 , line3 , line4]
    
    for i in [0 , 1 , 2 , 3]:
        line_len = len(lines[i])
        if line_len <= 20:
            lcd.lcd_display_string(lines[i], i+1)
        else:
            lines[i] = lines[i] + " " + lines[i]
            lcd.lcd_display_string(lines[i][line_pos[i]:20+line_pos[i]], i+1)
            line_pos[i] = line_pos[i] + 1
            if line_pos[i] > line_len:
                line_pos[i] = 0


update_display()

