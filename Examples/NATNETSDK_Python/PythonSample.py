#Copyright © 2018 Naturalpoint
#
#Licensed under the Apache License, Version 2.0 (the "License");
#you may not use this file except in compliance with the License.
#You may obtain a copy of the License at
#
#http://www.apache.org/licenses/LICENSE-2.0
#
#Unless required by applicable law or agreed to in writing, software
#distributed under the License is distributed on an "AS IS" BASIS,
#WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#See the License for the specific language governing permissions and
#limitations under the License.

# OptiTrack NatNet direct depacketization sample for Python 3.x
#
# Uses the Python NatNetClient.py library to establish a connection (by creating a NatNetClient),
# and receive data via a NatNet connection and decode it using the NatNetClient library.

from dronekit import connect, VehicleMode
from pymavlink import mavutil
import argparse
import time
from NatNetClient import NatNetClient


#######################

### To create a SITL, type in the terminal:   sim_vehicle.py -v ArduCopter -L ITA --console --map

#######################

### Create an argument to change which IP address will be connected.

parser = argparse.ArgumentParser()
parser.add_argument('--connect', default='udpin:161.24.4.61:14551') ## Or /dev/ttyPixhawk, 0.0.0.0:14551, 127.0.0.1:14553
args = parser.parse_args()


### Connect to the vehicle.

print("Connecting to the vehicle on: {}".format(args.connect))
vehicle = connect(args.connect, baud=921600, wait_ready=False)
mocap_msg = None;

time.sleep(2)
if(vehicle != None):
    print("Connected!")
else:
    print("Vehicle is NOT connected!")

### This is a callback function that gets connected to the NatNet client and called once per mocap frame.

def receiveNewFrame( frameNumber, markerSetCount, unlabeledMarkersCount, rigidBodyCount, skeletonCount,
                    labeledMarkerCount, timecode, timecodeSub, timestamp, isRecording, trackedModelsChanged ):
    print( "Received frame", frameNumber )


### This is a callback function that gets connected to the NatNet client. It is called once per rigid body per frame

time_usec = 0.0
qw = 0.0 ; qx = 0.0 ; qy = 0.0 ; qz = 0.0
px = 0.0
py = 0.0
pz = 0.0

def receiveRigidBodyFrame( id, position, rotation ):

    print( "Received frame for rigid body", id )
    print( "Received frame for rigid body", position )
    px =   position[0] # x
    py =   position[2] # z
    pz =  -position[1] # -y

    print( "Received frame for rigid body", rotation )
    qw =   rotation[3]
    qx =   rotation[0]
    qy =   rotation[2]
    qz =  -rotation[1]

    time_usec = int(round(time.time() * 1000000))

    ### To send an message via mavlink:
    ### Encode the message  
    mocap_msg = vehicle.message_factory.att_pos_mocap_encode(time_usec, [qw, qx, qy, qz], px, py, pz)

    ### Send via mavlink
    vehicle.message_factory.att_pos_mocap_send(time_usec, [qw, qx, qy, qz], px, py, pz)    

    ##vehicle.send_mavlink(mocap_msg)
    ##vehicle._master.mav.send(mocap_msg)

    time.sleep(0.01)

def MOCAP_Menssage():

    print ("Vehicle mode: {}".format(vehicle.mode.name))
    print ("---------------------------------")
    print (receiveRigidBodyFrame(id))
    print (mocap_msg)
    print (vehicle.on_message('ATT_POS_MOCAP'))
    time.sleep(0.5)

# This will create a new NatNet client

streamingClient = NatNetClient()

### Configure the streaming client to call our rigid body handler on the emulator to send data out.

streamingClient.rigidBodyListener = receiveRigidBodyFrame
streamingClient.newFrameListener = receiveNewFrame

### Start up the streaming client now that the callbacks are set up.

### This will run perpetually, and operate on a separate thread.

streamingClient.run()
