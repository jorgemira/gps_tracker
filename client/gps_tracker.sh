#! /bin/sh

### BEGIN INIT INFO
# Provides:          gps_tracker.py
# Required-Start:    $remote_fs $syslog
# Required-Stop:     $remote_fs $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
### END INIT INFO

# Carry out specific functions when asked to by the system
case "$1" in
  start)
    echo "Starting gps_tracker.py"
    /usr/local/bin/gps_tracker.py &
    ;;
  stop)
    echo "Stopping gps_tracker.py"
    pkill -f /usr/local/bin/gps_tracker.py
    ;;
  *)
    echo "Usage: /etc/init.d/gps_tracker.sh {start|stop}"
    exit 1
    ;;
esac

exit 0