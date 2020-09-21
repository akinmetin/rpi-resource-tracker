# Raspberry Pi Resource Monitor Service

## Getting Started

These instructions will help you to deploy and run the memory tracker service on a Raspberry Pi device.

This service will track the memory usage every second and if it detects more than 80% memory usage for 15 seconds, it will start to log the event.

## Prerequisites

Raspberry Pi device with OS (Debian Buster, version August 2020)


## Installing & Instructions

Copy ``monitor.py`` and ``requirements.txt`` into ``/home/pi/pitop`` folder.

Enter into ``/home/pi/pitop`` folder.

Run ``pip3 install -r requirements.txt``

Create and run a service using the codes below:
```bash
# Install Python script as a service
cd /lib/systemd/system/

sudo nano rpimonitor.service

# paste these lines in # tags into service file
[Unit]
Description=Monitor Service for High Memory Usage
After=multi-user.target

[Service]
Type=simple
ExecStart=/usr/bin/python3 /home/pi/pitop/monitor.py
Restart=on-abort

[Install]
WantedBy=multi-user.target
#

sudo chmod 644 /lib/systemd/system/rpimonitor.service
chmod +x /home/pi/pitop/monitor.py
sudo systemctl daemon-reload
sudo systemctl enable rpimonitor.service
sudo systemctl start rpimonitor.service
```

When the high memory usage event occurs, current running processes on 15th second will be logged into ``var/log/memorymonitor/processes`` folder with a unique ``process_log`` .txt file. This unique id can be found at date formatted .txt file in the root of log folder.

You can find which process used how much memory if you open specific event's ``process_log`` value in ``processes`` folder.
For example,

```
[START] High Memory Usage started at 17-09-2020 09:51:19, process_log=hqdn8agIHA
```
this line is written in ``17-09-2020.txt`` file and if you check ``var/log/memorymonitor/processes/hqdn8agIHA.txt`` file, you can see the processes at the starting moment in descending memory usage order.

As a 2nd method, this script can be scheduled to run at every reboot using cron job, but using service method is more healthy and efficient.


## 3rd Party Packages

I have used ``psutil`` library which enables programs/scripts to track processes and system resources.


## Testing

You can edit and use ``memory_consumer.py`` script to consume the device's memory intentionally. You also need to decrease 80% threshold value and seconds in ``monitor.py`` to test the script easier.

Test cases can be found in ``/tests`` folder and all test cases are passing.

Tested the live version on my Raspberry Pi 3 device with default Raspberry Pi OS(Debian Buster, version August 2020) installation and works without a problem.

## Resources

raspberry pi python script as service --> https://gist.github.com/emxsys/a507f3cad928e66f6410e7ac28e2990f

python eat memory intentionally --> https://stackoverflow.com/questions/6317818/how-to-eat-memory-using-python

python psutil get process --> https://thispointer.com/python-get-list-of-all-running-processes-and-sort-by-highest-memory-usage/

python get cpu/ram usage --> https://stackoverflow.com/questions/276052/how-to-get-current-cpu-and-ram-usage-in-python
