import serial
import time
import binascii
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT)
GPIO.setwarnings(False)
p = GPIO.PWM(11, 50)                                                                       # 通道为 11 频率为 50Hz

ser = serial.Serial("/dev/ttyAMA0",256000)

if not ser.isOpen():
    print("open failed")
else:
    print("open success: ")
    print(ser)

try:
    while True:
        count = ser.inWaiting()
        if count > 0:
            recv = ser.read(count)
            hex_str = binascii.hexlify(recv).decode()                                       #字符串转换
            hex_array = [int(hex_str[i:i+2], 16) for i in range(0, len(hex_str), 2)]        #十进制
            #hex_array = [hex_str[i:i+2] for i in range(0, len(hex_str), 2)]                #十六进制
            print(hex_array[1])                                                             #串口输出距离代表的数值
            p.start(0)
            if (hex_array[1]<201):
                p.ChangeDutyCycle(int(hex_array[1])/2)                                      #由于占空比只能到100，做缩小化处理
            else:
                p.ChangeDutyCycle(100)
            time.sleep(0.1) 
            ser.write(hex_array)                                                            #十进制
            #ser.write(binascii.unhexlify(''.join(hex_array)))                              #十六进制
        time.sleep(0.05) 
except KeyboardInterrupt:
    if ser != None:
        ser.close()