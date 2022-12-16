#!/usr/bin/env bash

################################################
#---------------- TigerVNC----------------------
################################################

echo "Installing TigerVNC server"

apt update
apt install -y tigervnc-standalone-server tigervnc-common tigervnc-xorg-extension xauth xinit 
dpkg --configure -a

apt-get clean -y

echo "Install noVNC - HTML5 based VNC viewer"
mkdir -p $NO_VNC_HOME/utils/websockify

apt-get install wget -y

wget -qO- https://github.com/novnc/noVNC/archive/refs/tags/v1.3.0.tar.gz | tar xz --strip 1 -C $NO_VNC_HOME
# use older version of websockify to prevent hanging connections on offline containers, see https://github.com/ConSol/docker-headless-vnc-container/issues/50
wget -qO- https://github.com/novnc/websockify/archive/refs/tags/v0.10.0.tar.gz | tar xz --strip 1 -C $NO_VNC_HOME/utils/websockify
#chmod +x -v $NO_VNC_HOME/utils/*.sh
## create index.html to forward automatically to `vnc_lite.html`

apt-get install python3 -y
