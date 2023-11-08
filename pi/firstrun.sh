#!/bin/bash

set +e

CURRENT_HOSTNAME=`cat /etc/hostname | tr -d " \t\n\r"`
if [ -f /usr/lib/raspberrypi-sys-mods/imager_custom ]; then
   /usr/lib/raspberrypi-sys-mods/imager_custom set_hostname telescope-5
else
   echo telescope-5 >/etc/hostname
   sed -i "s/127.0.1.1.*$CURRENT_HOSTNAME/127.0.1.1\ttelescope-5/g" /etc/hosts
fi
FIRSTUSER=`getent passwd 1000 | cut -d: -f1`
FIRSTUSERHOME=`getent passwd 1000 | cut -d: -f6`
if [ -f /usr/lib/raspberrypi-sys-mods/imager_custom ]; then
   /usr/lib/raspberrypi-sys-mods/imager_custom enable_ssh
else
   systemctl enable ssh
fi
if [ -f /usr/lib/userconf-pi/userconf ]; then
   /usr/lib/userconf-pi/userconf 'pi' '$5$PGV.wYaWdV$DIZIF4qfWsA4Lq7.7sED.rbCLlxoq.fW54WEfz9CO/1'
else
   echo "$FIRSTUSER:"'$5$PGV.wYaWdV$DIZIF4qfWsA4Lq7.7sED.rbCLlxoq.fW54WEfz9CO/1' | chpasswd -e
   if [ "$FIRSTUSER" != "pi" ]; then
      usermod -l "pi" "$FIRSTUSER"
      usermod -m -d "/home/pi" "pi"
      groupmod -n "pi" "$FIRSTUSER"
      if grep -q "^autologin-user=" /etc/lightdm/lightdm.conf ; then
         sed /etc/lightdm/lightdm.conf -i -e "s/^autologin-user=.*/autologin-user=pi/"
      fi
      if [ -f /etc/systemd/system/getty@tty1.service.d/autologin.conf ]; then
         sed /etc/systemd/system/getty@tty1.service.d/autologin.conf -i -e "s/$FIRSTUSER/pi/"
      fi
      if [ -f /etc/sudoers.d/010_pi-nopasswd ]; then
         sed -i "s/^$FIRSTUSER /pi /" /etc/sudoers.d/010_pi-nopasswd
      fi
   fi
fi
if [ -f /usr/lib/raspberrypi-sys-mods/imager_custom ]; then
   /usr/lib/raspberrypi-sys-mods/imager_custom set_wlan 'Sztehlo_Diak' '257f0245d098f0e24e6c6a663562ad70384c1d418c68f5133cebe8095d226560' 'HU'
else
cat >/etc/wpa_supplicant/wpa_supplicant.conf <<'WPAEOF'
country=HU
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
ap_scan=1

update_config=1
network={
	ssid="Sztehlo_Diak"
	psk=257f0245d098f0e24e6c6a663562ad70384c1d418c68f5133cebe8095d226560
}

WPAEOF
   chmod 600 /etc/wpa_supplicant/wpa_supplicant.conf
   rfkill unblock wifi
   for filename in /var/lib/systemd/rfkill/*:wlan ; do
       echo 0 > $filename
   done
fi
if [ -f /usr/lib/raspberrypi-sys-mods/imager_custom ]; then
   /usr/lib/raspberrypi-sys-mods/imager_custom set_keymap 'hu'
   /usr/lib/raspberrypi-sys-mods/imager_custom set_timezone 'Europe/Budapest'
else
   rm -f /etc/localtime
   echo "Europe/Budapest" >/etc/timezone
   dpkg-reconfigure -f noninteractive tzdata
cat >/etc/default/keyboard <<'KBEOF'
XKBMODEL="pc105"
XKBLAYOUT="hu"
XKBVARIANT=""
XKBOPTIONS=""

KBEOF
   dpkg-reconfigure -f noninteractive keyboard-configuration
fi

sudo echo "country=HU" >> /etc/wpa_supplicant/wpa_supplicant.conf
sudo echo "network={" >> /etc/wpa_supplicant/wpa_supplicant.conf
sudo echo "  ssid=\"Sztehlo_Diak\"" >> /etc/wpa_supplicant/wpa_supplicant.conf
sudo echo "  psk=\"*****\"" >> /etc/wpa_supplicant/wpa_supplicant.conf
sudo echo "  key_mgmt=WPA-PSK" >> /etc/wpa_supplicant/wpa_supplicant.conf
sudo echo "  id_str=\"school\"" >> /etc/wpa_supplicant/wpa_supplicant.conf
sudo echo "}" >> /etc/wpa_supplicant/wpa_supplicant.conf

sudo service wpa_supplicant restart

sleep 60

rm -f /boot/firstrun.sh
sed -i 's| systemd.run.*||g' /boot/cmdline.txt

wget -O - https://raw.githubusercontent.com/symat/sztehlo-telescope/main/pi/setup.sh | bash
exit 0
