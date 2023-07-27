# sztehlo-telescope
3D printed 150mm Newtonian telescope controlled by raspberry pi zero

## Windows environment setup

## git + mingw
 - download and install git for windows: https://gitforwindows.org/
 - path: git from command line and also from third party software
 - use bundled openssh
 - use openssl library
 - checkout windows style commit unix style
 - use mintty terminal
 - git pull behaviour: rebase
 - enable file system caching, disable symbolic links

## optional: download GUI for git:
 - download and install: https://tortoisegit.org/download/
 - git.exe path: C:\Program Files\Git\bin

## clone sztehlo-telescope reopsitory:
start git bash
cd /c/git
git clone https://github.com/symat/sztehlo-telescope.git

## download python on your machine
- download and use pythonn 3.9 (this is the version used on the PI currently): https://www.python.org/downloads
 - choose "Windows installer (64-bit)"
 - install with IDLE

## setup raspberry PI zero
 - download: Raspberry PI Imager (https://www.raspberrypi.com/software/)
 - flush the SD card: 
    - choose OS: Rapsberry PI OS (other) -> Rapsberry PI OS light (32 bit)
    - choose your SD card
	- options (gear icon): 
	   - set hostname: telescope-1 
	   - set username: pi
	   - set password: ... (don't forget!)
	   - configure WIFI
	   - set local (hungarian keyboard)
	- write
 - add empty `ssh` file to enable ssh`
 - add `wpa_supplicant.conf` to setup WIFI (see example HERE)
 - start the PI with the SD card
 - find out the IP (e.g. port scanner, or router admin)
 

 - start git bash and ssh to the IP
   - command like: `ssh pi@192.168.x.y`
   - user was `pi`, password was ...
   - you can change password later: `passwd`
 - if WIFI doesn't work, copy the wpa_supplicant.conf (TODO link) file to the SD card
 - if you can ssh, but later you want to edit WIFI settings, or add more WIFI networks, edit the wpa_supplicant.conf  (TODO link)  file on the raspberry PI: `sudo vi /etc/wpa_supplicant/wpa_supplicant.conf`
 - run first-time setup: `wget -O - https://raw.githubusercontent.com/symat/sztehlo-telescope/main/pi/setup.sh | bash`
   
