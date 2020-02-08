import time
import IMU
import socket
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
send_data = ""

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


while truth == True:
    ACCx = IMU.readACCx()*.244/1000
    ACCy = IMU.readACCy()*.244/1000
    ACCz = IMU.readACCz()*.244/1000
    print("X = "+str(ACCx)+"G     "+"Y = "+str(ACCy)+"G     "+"Z = "+str(ACCz)+"G     ")
    print("Time is: " +str(time.time() - start))


    if ((ACCx>6) or (ACCy>6)):
        if ACCy>ACCx:
            print("cutting motion detected")
            cut_num = cut_num+1
            cut = True
        if ACCx>ACCy:
            print("cooking motion detected")
            cook_num = cook_num+1
            cook = True



    if(cut == True):
        send_data = "chop"
        cut = False

    if(cook == True):
        send_data = "cook"
        cook = False

    client.sendto(send_data.encode(), ('172.20.10.6',8080))



    """
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
        if ACCy>6:
            #cut_num = cut_num+1
            print("chop")
            send_data = "chop"

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

        """

    time.sleep(0.35)
