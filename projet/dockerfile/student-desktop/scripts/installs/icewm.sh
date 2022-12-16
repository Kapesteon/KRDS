#!/bin/bash

#Remove Pre-installted GUI component
apt-get update 
apt-get remove -y --auto-remove desktop-base
apt-get remove -y --auto-remove gnome-*  
apt-get remove -y --auto-remove nautilus nautilus-* 
apt-get autoremove    

echo "Install IceWM UI components"
apt-get update
apt-get install -y supervisor icewm xterm xfonts-base xauth xinit dbus-x11 libdbus-glib-1-2
apt-get purge -y pm-utils *screensaver*
apt-get clean -y
