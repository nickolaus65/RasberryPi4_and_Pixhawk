<h1>
RasberryPi4_Pixhawk.
</h1>
<p>
This report instructs how to make the connection between a Pixhawk PX4 and a Raspberry Pi 4 using the MAVLink Protocol to control the drone remotely and see it information.
  
The information below is valid only to the OS: **Linux (recommend Ubuntu 20.04).**
</p>
<h3>
  1. Connect the Pixhawk with QGroundControl and configure the following Pixhawk parameters:
</h3>

---
<p>

**SERIAL2_PROTOCOL = 1 (Mavlink 1 = 1 or Mavlink 2 = 2)**

**SERIAL2_BAUD = 921 (baud rate = 921600)**

**EKF2_AID_MASK = use optical flow only**

**CBRK_SUPPLY_CHK = no check**

**CBRK_USB_CHK = no check**

**MAV_0_CONFIG = TELEM 2**

**MAV_0_MODE = Onboard**

**MAV_0_RATE = 1200 B/s**

**COM_OBL_ACT = land**

**COM_OBL_RC_ACT = land**

**CBRK_IO_SAFETY = no check**
</p>
<h3>
2.	Using jumpers, connect the TELEM 2 (Pixhawk) via USB-Serial adapter to an USB on the Raspberry Pi 4.
</h3>

---
**See the link below for more information:**
https://dev.px4.io/master/en/companion_computer/pixhawk_companion.html#hardware-setup

<h3>
  3.	Run the code below to see which USB port the Pixhawk is connected: 
</h3>

---
```
lsusb
```

The device ID is important to the next step (the ID number is likely to change);

<h3>
4.	Run the line below to change the USB rules:
</h3>

---
```
sudo nano /etc/udev/rules.d/99-pixhawk.rules
```
<h3>
5.	Enter this line with the correct ID code:
</h3>

---
```
SUBSYSTEM=="tty", ATTRS{idVendor}=="0403", ATTRS{idProduct}=="6001", SYMLINK+="ttyPix4"
```
<h3>
6.	Run these commands to update and upgrade the packages in the Raspberry Pi 4 : sudo apt-get update
</h3>

sudo apt-get upgrade

sudo apt-get install screen python-wxgtk3.0 python-matplotlib python-opencv python-pip python-numpy python-dev libxml2-dev libxslt-dev
<pre><code>

$	sudo pip3 install future
$	sudo pip3 install pymavlink
$	sudo pip3 install mavproxy
$	sudo reboot now     (This step is necessary to compile all the changes)

</code>
</pre>

7.	Test the connection between Pixhawk and Raspberry Pi 4: 
sudo -s


mavproxy.py --master=/dev/ttyPix4 --baudrate 921600 --out=udp:192.168.0.102:14550 --out=udp:192.168.0.103:14550 --aircraft MyCopter
(*--aircraft will be the folder to store the logs files.)
8.	Install SSH on a Linux machine: 
sudo apt-get install ssh
or
sudo apt-get install openssh-client

9.	Enable SSH on Raspberry Pi 4: 
raspi-config

10.	Go to [ Interfacing Options > SSH > Yes > Finish ]. And now reboot:

sudo reboot now


11.	In the Host pc, another LINUX computer, install the MAVproxy and DroneKit: 
sudo -H
pip3 install mavproxy
sudo -H pip3 install dronekit
sudo -H pip3 install pymavlink

12.	Clone the dronekit-python repository in the host pc (Linux recommended): 
git clone https://github.com/dronekit/dronekit-python.git

13.	Use the code magnetometer.py in the folder Examples/ to take the values of the magnetometer sensor.

14.	Type this line to connect to Pixhawk: 
python3 mag_pix4.py --connect "192.168.0.103:14551"

