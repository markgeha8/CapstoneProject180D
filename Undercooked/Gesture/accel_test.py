import time
import IMU
IMU.detectIMU()#Detect if BerryIMUv1 or BerryIMUv2 is connected.
IMU.initIMU()#Initialise the accelerometer, gyroscope and compass
truth = True

cut = False
cut_num = 0
near_block = False
cook = False
cook_num = 0
near_stove = False
start = 0
md = False
start = time.time()



while truth == True:
    ACCx = IMU.readACCx()*.244/1000
    ACCy = IMU.readACCy()*.244/1000
    ACCz = IMU.readACCz()*.244/1000
    print("X = "+str(ACCx)+"G     "+"Y = "+str(ACCy)+"G     "+"Z = "+str(ACCz)+"G     ")
    print("Time is: " +str(time.time() - start))

    #initial detection
    if ((ACCx>5) or (ACCy>5)) and (md==False) and (cut==False) and (cook==False):
        if ACCy>5 and md == False:
            print("cutting motion detected")
            cut_num = cut_num+1
            cut = True
        if ACCx>5 and md == False:
            print("cooking motion detected")
            cook_num = cook_num+1
            cook = True
        md = True
        start = time.time()

    #Cutting - must cut 10 motions to be done
    if (cut == True) and (time.time()-start < 6):
        if ACCy>5:
            cut_num = cut_num+1
            print("cutting motion detected" + str(cut_num) + "/10")
        if cut_num == 10:
            print("ingredient cut")
            start = time.time()
            cut_num = 0
            cut = False
            cook_num = 0
            cook = False
            md = False
            truth = False


    #Cooking - must cook 10 motions to be done
    if (cook == True) and (time.time()-start < 6):
        if ACCx>4:
            cook_num = cook_num+1
            print("cooking motion detected" + str(cook_num) + "/10")
        if cook_num == 20:
            print("ingredient cooked")
            start = time.time()
            cut_num = 0
            cut = False
            cook_num = 0
            cook = False
            md = False
            truth = False


    #Reset Timer if takes too long
    if((cook==True) or (cut == True)) and (time.time()-start > 7):
        start = time.time()
        print("took too long")
        truth = false



    time.sleep(0.03)
