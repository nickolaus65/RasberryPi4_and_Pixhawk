from dronekit import connect, VehicleMode, LocationGlobalRelative
from pymavlink import mavutil
import PySimpleGUI as spg
import numpy as np
import time
import argparse

### Argument to read the IPaddress setted on MAVProxy command.

parser = argparse.ArgumentParser()
parser.add_argument('--connect', default='0.0.0.0:14550')
args = parser.parse_args()

### Connect to the Vehicle.

print ("Connecting to vehicle on: %s" % args.connect)
vehicle = connect(args.connect, baud=921600, wait_ready=False)

### GUI to show the changes on the Magnetometer axis. 

debugfile = 'exp1.txt'
num = 1
spg.theme('DarkAmber')


layout =[
    [spg.Text('Magnetometer Recording:', size=(22,2))], 
    [spg.Text('File: exp1.txt', size=(22,1), key='file')], 
    [spg.Text('Read to record!', size=(22,2), key='_wait_')], 
    [
        spg.Button('Start', size=(4,2), key='start'), 
        spg.Text('     '), 
        spg.Button('Exit', size=(4,2))]
    ]

window = spg.Window('MAG', layout)

#Magnetometer axis gathering.
timeout = 10    #[seconds]

while True:   
    event, values = window.Read()

    if event in (None, 'Exit'): break

    if event == 'start':

        file = open(debugfile,'w')
        num +=1
        debugfile = 'exp{}.txt'.format(num)
        window.Element('file').Update('File: {}'.format(debugfile))
        

        mag_axis = [
            vehicle._master.messages['RAW_IMU'].xmag,
            vehicle._master.messages['RAW_IMU'].ymag,
            vehicle._master.messages['RAW_IMU'].zmag
            ]
        file.write(str(mag_axis)+'\n')

        t_start = time.time()
        while time.time() <= t_start + timeout: 
            print ('mag_X: {0}  mag_Y: {1}  mag_Z: {2}'.format(
                vehicle._master.messages['RAW_IMU'].xmag,
                vehicle._master.messages['RAW_IMU'].ymag,
                vehicle._master.messages['RAW_IMU'].zmag
            ))

            mag_axis = [
                vehicle._master.messages['RAW_IMU'].xmag,
                vehicle._master.messages['RAW_IMU'].ymag,
                vehicle._master.messages['RAW_IMU'].zmag
            ]
            file.write(str(mag_axis)+'\n')

            print(time.time())
            time.sleep(0.1)
        file.close()

        if t_start + timeout < time.time(): 
            print('Data recording completed!\n Elapsed Time: {} miliseconds'.format(timeout*10))

