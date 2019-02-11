import serial
import time
from imu_commands import model_name,get_serial_number,get_imu_data,read_reg,accelDisturbance

ser=serial.Serial("COM12")
print(ser.name)
ser.baudrate=9600


model_name(ser)
get_serial_number(ser)
# get_imu_data(ser)
# read_reg(ser,27)
read_reg(ser,27)
# accelDisturbance(ser,0)
ser.close()