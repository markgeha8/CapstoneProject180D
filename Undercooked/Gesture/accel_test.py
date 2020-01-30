import time
import IMU
IMU.detectIMU()#Detect if BerryIMUv1 or BerryIMUv2 is connected.
IMU.initIMU()#Initialise the accelerometer, gyroscope and compass
truth = True

cut = False
cut_num = 0
cook = False
cook_num = 0
start = 0
md = False


while truth == True:
    ACCx = IMU.readACCx()*.244/1000
    ACCy = IMU.readACCy()*.244/1000
    ACCz = IMU.readACCz()*.244/1000
    print("X = "+str(ACCx)+"G     "+"Y = "+str(ACCy)+"G     "+"Z = "+str(ACCz)+"G     ")
    print("Time is: " +str(time.time() - start))

    #initial detection
    if (ACCx>3) or (ACCy>3) and (md==False):
        if ACCy>3:
            print("cutting motion detected")
            cut = True
        if ACCx>3:
            print("cooking motion detected")
            cut = True
        md = True
        start = time.time()

    #Cutting - must cut 5 motions to be done
    if (cut == True) and (time.time()-start > 7):
        if ACCy>3:
            print("cutting motion detected")
            cut_num = cut_num+1
        if cut_num == 10:
            print("ingredient cut")
            truth = False
            start = time.time()



    time.sleep(0.03)
