#!/bin/bash
sudo mount /dev/sdb1 /media/usb
sudo cat /var/log/dmesg > /media/usb/logs/dmesg.log
sudo cat /var/log/boot.log > /media/usb/logs/boot.log
sudo umount /media/usb
echo "USB device added at $(date)" >>/tmp/scripts.log
