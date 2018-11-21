#!/bin/sh
# lcd.sh	Shows info about Cluster on LCD.
#
# Version:	@(#)lcd.sh  1.00  19-Nov-2018  tobias.boese@accenture.com
#

### BEGIN INIT INFO
# Provides:          lcd
# Required-Start:    
# Required-Stop:     
# Should-Stop:       
# Default-Start:     S
# X-Start-Before:    
# Default-Stop:      0 6
# Short-Description: Shows info about Cluster on LCD.
### END INIT INFO


lcdsh()
{

    case "$1" in
	start)
	    nohup sudo -u pi python3 /home/pi/PiClusterLcd/lcd.py &
		;;
	stop|restart)

	    ;;
	*)
	    log_success_msg "Usage: lcd.sh {start|stop|restart}"
	    log_success_msg "       start sets kernel (system) clock from hardware (RTC) clock"
	    log_success_msg "       stop and reload set hardware (RTC) clock from kernel (system) clock"
	    return 1
	    ;;
    esac
}

lcdsh "$@"
