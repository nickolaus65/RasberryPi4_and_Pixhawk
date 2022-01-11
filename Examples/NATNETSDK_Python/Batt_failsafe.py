### This code allows you to create a battery failsafe to the connected drone

### Run with SITL
# Type the line in the terminal:
# sim_vehicle.py -v ArduCopter -L ITA --console

### Importing librarys

from dronekit import connect, VehicleMode
from pymavlink import mavutil
import argparse
import time
import os

### Create an argument to change whinch IP address will be connected

parser = argparse.ArgumentParser()
parser.add_argument('--connect', default='127.0.0.1:14551') # Or 192.168.0.104:14551 , /dev/ttyPixhawk , 127.0.0.1:14551
args = parser.parse_args()

### Connect to the vehicle.

print("Connect to the vehicle on: {}".format(args.connect))
vehicle = connect(args.connect, baud=921600, wait_ready=False)

### Setting the vehicle's mode to Stabilized.

vehicle.mode = VehicleMode("STABILIZE")

initial_time = time.time()
time.sleep(5)

### Deleting the old and creating a new data storage file.

if os.path.exists("battery_data.txt"):

    os.remove("battery_data.txt")
    print("Creating file.")
    time.sleep(1)
    file = open('battery_data.txt', 'w')
else :

    print("Creating file.")
    time.sleep(1)
    file = open('battery_data.txt', 'w')

batt_data = []      ### List to the data. 
charge_remaining = 0.0
### Funtion to store the data in the list.

def battery_data():

    charge_remaining = (2200.0 * vehicle.battery.level)/100.0  # Formula to show the remaining energy.
    ### Showing the data values.

    print("=========================")
    print("  Battery voltage: {:.3f}V".format(vehicle.battery.voltage))
    print("  Battery level: {0}% = {1}mAh".format(vehicle.battery.level, charge_remaining))
    print("  Battery current: {}mA".format(vehicle.battery.current))
    print("  Battery consumed current: {}mAh".format(vehicle._master.messages['BATTERY_STATUS'].current_consumed))

    ### Storing the data in the list.
    final_time = time.time()
    elap_time  = final_time - initial_time
    
    batt_data = [
        "Battery voltage: {:.3f}V".format(vehicle.battery.voltage),
        "Battery current: {}mA".format(vehicle.battery.current),
        "Time: {:.0f}s".format(elap_time),
        "Battery level: {0}% = {1}mAh".format(vehicle.battery.level, charge_remaining),      
        "Battery consumed current: {}mAh".format(vehicle._master.messages['BATTERY_STATUS'].current_consumed)
    ]

    ### Writing the list in the file.

    file.write(str(batt_data) + '\n')


### Loop to show and store data.

elap_time = 0.0

while (True):

    if (vehicle.armed == True):
        
        battery_data()
        time.sleep(1)
              
    ### Set to landing (LAND) mode if the voltage is 10.355V.

    if (vehicle.battery.voltage == 10.35):

        print("!!! CRITICAL BATTERY VOLTAGE = {}V !!!".format(vehicle.battery.voltage))
        print("Landing...")
        vehicle.mode = VehicleMode("LAND")
        
        if ((vehicle.mode.name == "LAND") & (vehicle.armed == False)):
            
            print("LANDED")
            print("Storage data completed, go to 'batt_data.txt' to see it.")
            vehicle.mode = VehicleMode("STABILIZE")
            
            file.close()
            time.sleep(1)
            break

final_time = time.time()
elap_time  = final_time - initial_time
print("Time Flying: {:.0f}s".format(elap_time))

vehicle.close()