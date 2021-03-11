git clone https://github.com/hzeller/rpi-rgb-led-matrix.git

sudo pip install bs4

cd
cd /home/pi/rpi-rgb-led-matrix

sudo apt-get update && sudo apt-get install python3-dev python3-pillow -y
make build-python PYTHON=$(which python3)
sudo make install-python PYTHON=$(which python3)

cd
