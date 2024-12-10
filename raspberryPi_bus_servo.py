# -*- coding:UTF-8 -*-
import RPi.GPIO as GPIO
import time
import string
import serial


global ser

# 设置GPIO口为BCM编码方式
GPIO.setmode(GPIO.BCM)

# 忽略警告信息
GPIO.setwarnings(False)


# 控制舵机，index为舵机的ID号，value为舵机的位置，s_time为舵机的运行时间
def Servo_control(index, value, s_time):
    pack1 = 0xff
    pack2 = 0xff
    id = index & 0xff
    len = 0x07
    cmd = 0x03
    addr = 0x2A
    pos1 = (value >> 8) & 0x00ff
    pos2 = value & 0x00ff
    time1 = (s_time >> 8) & 0x00ff
    time2 = s_time & 0x00ff
    checknum = (~(id + len + cmd + addr + pos1 + pos2 + time1 + time2)) & 0xff

    data = [pack1, pack2, id, len, cmd, addr,
            pos1, pos2, time1, time2, checknum]
    ser.write(bytes(data))


# 设置舵机ID号
def Servo_Set_ID(index):
    if index < 1 or index > 250:
        return None

    pack1 = 0xff
    pack2 = 0xff
    id = 0xfe
    len = 0x04
    cmd = 0x03
    addr = 0x05
    set_id = index & 0xff

    checknum = (~(id + len + cmd + addr + set_id)) & 0xff

    data = [pack1, pack2, id, len, cmd, addr, set_id, checknum]
    ser.write(bytes(data))



try:
    ser = serial.Serial("/dev/ttyS0", 115200, timeout=0.001)
    print ("serial.isOpen()")
    index = 0x01
    Servo_Set_ID(index)
    time.sleep(.01)

    while True:
        Servo_control(index, 3100, 1000)
        time.sleep(2)
        Servo_control(index, 900, 1000)
        time.sleep(2)

except KeyboardInterrupt:
    pass
ser.close()
GPIO.cleanup()
