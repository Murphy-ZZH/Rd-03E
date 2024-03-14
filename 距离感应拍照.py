import serial
import time
import binascii
import RPi.GPIO as GPIO
from picamera import PiCamera
from time import sleep
import _thread
import threading
threadLock = threading.Lock()
#####################GPIO设置#####################
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT)
GPIO.setwarnings(False)
p = GPIO.PWM(11, 50)                                                                       # 通道为 11 频率为 50Hz

#####################串口设置#####################
ser = serial.Serial("/dev/ttyAMA0",256000)
#####################摄像头设置#####################
camera = PiCamera()
#####################变量设置#####################
global i
i=0
n=0
j=0
#####################多线程设置#####################
class Camera_Shot:
    def __init__(self,I):
        print('拍照线程启动')
        self.i = I
        _thread.start_new_thread(self.shot, ())
    def shot(self):
        threadLock.acquire()
        camera.capture('/home/murphy/image' + str(self.i) + '.jpg')                                    #拍照
        print("拍照成功"+str(i))
        threadLock.release()
#####################主程序#####################
if not ser.isOpen():
    print("open failed")
else:
    print("open success: ")
    print(ser)
try:
    while True:
        p.start(0)
        count = ser.inWaiting()
        if count > 0:
            recv = ser.read(count)
            hex_str = binascii.hexlify(recv).decode()                                       #字符串转换
            hex_array = [int(hex_str[i:i+2], 16) for i in range(0, len(hex_str), 2)]        #十进制
            #hex_array = [hex_str[i:i+2] for i in range(0, len(hex_str), 2)]                #十六进制
            if len(hex_array) > 1:
                if hex_array[1] > 100:
                    #p.ChangeDutyCycle(int(hex_array[1])/2)                                      #由于占空比只能到100，做缩小化处理
                    print('距离过远' + str(hex_array[1]) + 'cm')
                elif hex_array[1] < 101 and hex_array[1] > 0:
                    n = n + 1
                    print('准备拍照' + str(hex_array[1]) + 'cm')
                    if n > 10:
                        n = 0
                        p.ChangeDutyCycle(100)
                        Shot_ON = Camera_Shot(i)
                        i = i + 1
                        if i > 100:
                            i = 0
                else:
                    #p.ChangeDutyCycle(50)
                    print('未检测到运动物体')
                    j = j + 1
                    if j > 3:
                        n = 0
                        j = 0 
            #ser.write(hex_array)                                                            #十进制
            #ser.write(binascii.unhexlify(''.join(hex_array)))                              #十六进制
        time.sleep(0.1) 
except KeyboardInterrupt:
    if ser != None:
        ser.close()
