# install web server 
pip3 install Flask


sudo apt-get install -y git

cd /home/pi/
git clone https://github.com/symat/sztehlo-telescope.git

sudo cp /home/pi/sztehlo-telescope/pi/oled-web-server.service /lib/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable oled-web-server.service
