```shell script
sudo mv gps_tracker.py /usr/local/bin/

sudo mkdir /usr/local/share/gps_tracker

sudo chmod +x /usr/local/bin/gps_tracker.py

sudo mv gps_tracker.sh /etc/init.d/

sudo chmod +x /etc/init.d/gps_tracker.sh

sudo update-rc.d gps_tracker.sh defaults

sudo /etc/init.d/gps_tracker.sh start
```
