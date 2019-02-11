# a prototype for IMU data extraction
# uses default settings 
# connected to COM7, (change that for corresponding port)

import serial
import time
ser=serial.Serial("COM7")
print(ser.name)
ser.baudrate=115200

Data={}
def read_imu(ser):
	"""
		Read Imu data into a dictionary
		returns a dictionary 
		with following keys "Yaw","Pitch","Roll","MagX","MagY","MagZ","AccX","AccY","AccZ","GyroX","GyroY","GyroZ"
		# >>>print(read_imu["Yaw"])

	"""
	while True:
		x=str(ser.readline()).split(",")
		i=1
		# Yaw	Pitch	Roll	MagX	MagY	MagZ	AccX	AccY	AccZ	GyroX	GyroY	GyroZ
		elements=["Yaw","Pitch","Roll","MagX","MagY","MagZ","AccX","AccY","AccZ","GyroX","GyroY","GyroZ"]
		if i+len(elements)<=len(x) and x[0]=="b'$VNYMR":
			index=1
			for data in elements:
				if data!="GyroZ":
					Data[data]=x[index]
				else:
					Data[data]=x[index].split("*")[0]
				index=index+1
			return Data
			ser.close()
		# time.sleep(1)
	else:
		return None

	
print(read_imu(ser))
ser.close()
