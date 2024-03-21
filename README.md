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
```
start git bash
cd /c/git
git clone https://github.com/symat/sztehlo-telescope.git
```

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
	   - set local (hungarian keyboard)
	   - these would be nice, but doesn't work for some reason to me on the OS light version:
	      - configure WIFI
	      - enable ssh with passwork aduthentication
       - disabling the “Eject media when finished” (was recommended on posts)
	- write
   - wait for the `firstrun.sh` to appear on the card before ejecting
 - start the PI with the SD card, attach HDMI and keyboard (start takes 5-6 minutes, will restart multiple times) and add the wpa config manually
 - or if WIFI connection worked, then find out the IP (e.g. port scanner, or router admin)
 

if you need to add / change WPA config:
```
sudo nano /etc/wpa_supplicant/wpa_supplicant.conf

'''
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
country=HU

network={
     ssid="Sztehlo_Diak"
     psk="REDACTED"
     key_mgmt=WPA-PSK
     id_str="school"
}
'''

sudo service wpa_supplicant restart

ifconfig
```

But sometimes wpa_supplicant didn't work with me and e.g. to change the wifi network, I did change the wpa_supplicant.conf, plus also used networkManager:
```
sudo nmcli c delete "oldSSID"
sudo nmcli device wifi con "newSSID" password "REDACTED"
```
Maybe we could remove the whole wpa_supplicant stuff from the firstrun.sh and switch fully to networkmanager?

## SSH to the pi, using mingw + ssh
 - start git bash and ssh to the IP
   - command like: `ssh pi@192.168.x.y`
   - user was `pi`, password was ...
   - you can change password later: `passwd`
 - if WIFI doesn't work, copy the wpa_supplicant.conf (TODO link) file to the SD card
 - if you can ssh, but later you want to edit WIFI settings, or add more WIFI networks, edit the wpa_supplicant.conf  (TODO link)  file on the raspberry PI: `sudo vi /etc/wpa_supplicant/wpa_supplicant.conf`

 ## run first-time setup
 `wget -O - https://raw.githubusercontent.com/symat/sztehlo-telescope/main/pi/setup.sh | bash`


## test rapsberry py dashboard
test the dashboard:
```
  curl.exe -X POST -H "Content-type: application/json" -d "{ \"ip\":\"192.168.111.222\", \"message\":\"hello world\\n__ wrap after 30 chars _______here___\"}" "http://127.0.0.1:5000/messages/1"
```

test on PI:
```
systemctl status oled
journalctl -u oled -n 200
journalctl -u oled -f
echo "dfgsg" > /home/pi/oled
echo -e 'multi\nline' > /home/pi/oled
```

if oled display not works, enable I2C manually:
```
sudo raspi-config
go: Interfacing Options >> I2C >> enable ARM I2C interface
```


## connecting via USB (didn't work for me)

https://www.makeuseof.com/how-to-connect-raspberry-pi-to-laptop-or-pc-usb/

install bonjur
install RNDIS driver