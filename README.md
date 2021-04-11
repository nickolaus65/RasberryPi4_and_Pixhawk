<h1>
  RasberryPi4_Pixhawk.
</h1>
<p>
This report instructs how to make the connection between a Pixhawk PX4 and a Raspberry Pi 4 using the MAVLink Protocol to control the drone remotely and see it information.
  
The information below is valid only to the OS: **Linux (recommend Ubuntu 20.04).**
</p>
<h3>
 # Pixhawk:
</h3>
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
  2. Telemetry connection.
</h3>

---
Using jumpers, connect the TELEM 2 (Pixhawk) via USB-Serial adapter to an USB on the Raspberry Pi4.
**See the link below for more information:**

https://dev.px4.io/master/en/companion_computer/pixhawk_companion.html#hardware-setup
<h3>
<h3>
 # Raspberry Pi4:
</h3>
  3. Run the code below to see which USB port the Pixhawk is connected: 
</h3>

---
<pre>
  <code>$ lsusb
</code></pre>
<p>
  The device ID is important to the next step (the ID number is likely to change);
</p>
<h3>
  4. Run the line below to change the USB rules:
</h3>

---
<pre>
  <code>$ sudo nano /etc/udev/rules.d/99-pixhawk.rules
</code></pre>
<h3>
  5. Enter this line with the correct ID code:
</h3>

---
<pre>
  <code>$ SUBSYSTEM=="tty", ATTRS{idVendor}=="0403", ATTRS{idProduct}=="6001", SYMLINK+="ttyPix4"
</code></pre>
<h3>
6. Run these commands to update and upgrade the packages in the Raspberry Pi 4 : 
</h3>
<pre>
  <code>$ sudo apt-get update
  $ sudo apt-get upgrade
  $ sudo apt-get install screen python-wxgtk3.0 python-matplotlib python-opencv python-pip python-numpy python-dev libxml2-dev libxslt-dev
  $ sudo pip3 install future
  $ sudo pip3 install pymavlink
  $ sudo pip3 install mavproxy
  $ sudo reboot now   (This step is necessary to compile all the changes)
</code></pre>
<h3>
  7. Test the connection between Pixhawk and Raspberry Pi 4: 
</h3>

---
<pre>
  <code>$ sudo su
  $ mavproxy.py --master=/dev/ttyPix4 --baudrate 921600 --out=udp:192.168.0.102:14550 --out=udp:192.168.0.103:14550 --aircraft MyCopter
  ("--aircraft" will be the folder to store the logs files.)
</code></pre>
<h3>
8. Install SSH on a Linux machine:
</h3>

---
<pre>
  <code>$ sudo apt-get install ssh
</code></pre>
or
<pre>
  <code>$ sudo apt-get install openssh-client
</code></pre>
<h3>
  9. Enable SSH on Raspberry Pi 4:
</h3>
  
---
<pre>
  <code>$ raspi-config
</code></pre>

<h3>
  10. Go to [ Interfacing Options > SSH > Yes > Finish ]. And now reboot:
</h3>

---
<pre>
  <code>$ sudo reboot now
</code></pre>
<h3>
  11. In the Host pc, another LINUX computer, install the MAVproxy and DroneKit:
</h3>

---
<pre>
  <code>$ sudo -H pip3 install mavproxy
  $ sudo -H pip3 install dronekit
  $ sudo -H pip3 install pymavlink
  $ sudo -H pip3 install pymavlink
</code></pre>
<h3>
  12. Clone the dronekit-python repository in the Host PC (Linux recommended): 
</h3>

---
<pre>
  <code>$ git clone https://github.com/dronekit/dronekit-python.git
</code></pre>
<h3>
  13. Use the code magnetometer.py in the folder Examples/ to take the values of the magnetometer sensor.
</h3>

---
<h3>
  14. Type this line to connect to Pixhawk: 
</h3>

---
<pre>
  <code>$ python3 mag_pix4.py --connect "192.168.0.103:14551"
</code></pre>
