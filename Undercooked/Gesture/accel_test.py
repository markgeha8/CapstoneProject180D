import time
import IMU


IMU.detectIMU()     #Detect if BerryIMUv1 or BerryIMUv2 is connected.
IMU.initIMU()       #Initialise the accelerometer, gyroscope and compass

truth = True

while truth == True:


	#Read the accelerometer,gyroscope and magnetometer values
	ACCx = IMU.readACCx()* .244/1000
	ACCy = IMU.readACCy()* .244/1000
	ACCz = IMU.readACCz()* .244/1000

    print("##### X = %f G  #####" % (ACCx),
	print(" Y =   %fG  #####" % (ACCy),
	print(" Z =  %fG  #####" % (ACCz)

    if(ACCx > 2 | ACCy > 2 | ACCz >2)
        print("motion detected")
        truth = False





	#slow program down a bit, makes the output more readable
	time.sleep(0.03)
