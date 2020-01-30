import smbus
import time
import math
from LSM9DS0 import *
import datetime
bus = smbus.SMBus(1)




def writeACC(register,value):
        bus.write_byte_data(ACC_ADDRESS , register, value)
        return -1




def readACCx():
        acc_l = bus.read_byte_data(ACC_ADDRESS, OUT_X_L_A)
        acc_h = bus.read_byte_data(ACC_ADDRESS, OUT_X_H_A)
    acc_combined = (acc_l | acc_h <<8)

    return acc_combined  if acc_combined < 32768 else acc_combined - 65536


def readACCy():
        acc_l = bus.read_byte_data(ACC_ADDRESS, OUT_Y_L_A)
        acc_h = bus.read_byte_data(ACC_ADDRESS, OUT_Y_H_A)
    acc_combined = (acc_l | acc_h <<8)

    return acc_combined  if acc_combined < 32768 else acc_combined - 65536


def readACCz():
        acc_l = bus.read_byte_data(ACC_ADDRESS, OUT_Z_L_A)
        acc_h = bus.read_byte_data(ACC_ADDRESS, OUT_Z_H_A)
    acc_combined = (acc_l | acc_h <<8)

    return acc_combined  if acc_combined < 32768 else acc_combined - 65536





#initialise the accelerometer
writeACC(CTRL_REG1_XM, 0b01100111) #z,y,x axis enabled, continuos update,  100Hz data rate
writeACC(CTRL_REG2_XM, 0b00011000) #+/- 8G full scale



while True:


    #Read the accelerometer,gyroscope and magnetometer values
    ACCx = readACCx()
    ACCy = readACCy()
    ACCz = readACCz()

    print("##### X = %f G  #####" % ((ACCx * 0.244)/1000)),
    print(" Y =   %fG  #####" % ((ACCy * 0.244)/1000)),
    print(" Z =  %fG  #####" % ((ACCz * 0.244)/1000))



    #slow program down a bit, makes the output more readable
    time.sleep(0.03)
