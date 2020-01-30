import time
import IMU
IMU.detectIMU()#Detect if BerryIMUv1 or BerryIMUv2 is connected.
IMU.initIMU()#Initialise the accelerometer, gyroscope and compass
truth = True
while truth == True:
    ACCx = IMU.readACCx()*.244/1000
    ACCy = IMU.readACCy()*.244/1000
    ACCz = IMU.readACCz()*.244/1000
    print("X = "+ACCx+"G     "+"Y = "+ACCy+"G     "+"Z = "+ACCz+"G     ")
    if(ACCx>2 or ACCy>2 or ACCz >2)
        print("motion detected")
        truth = False
    time.sleep(0.03)
