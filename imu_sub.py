# a prototype for IMU data extraction
# uses default settings 
# connected to COM7, (change that for corresponding port)

import serial
import time

#  setup
ser=serial.Serial("COM7")
print(ser.name)
ser.baudrate=9600

# commands.add({'$VNb'RRG,1*9527'})'
cmd_model=b'$VNRRG,1*9527'

RREG={}
RREG.update({54:["IMU",["Magx","MagY","MagZ","AccelX","AccelY","AccelZ","GyroX","GyroY","GyroZ","Temp","Pressure"]]})
RREG.update({80:["Delta theta and velocity",["DeltaTime","DeltaThetaX","DeltaThetaY","DeltaThetaZ","DeltaVelocitx","DeltaVolocityY","DeltaVolocityZ"]]})


def write(cmd):
	"""Write a command to the sensor """
	# if b"\r" in cmd:
	print(">",str(cmd))
	ser.write(cmd)
	

	# time.sleep(1)
def get_imu_data():
	ser.reset_input_buffer()
	cmd=b'$VNRRG,54*XX\r\n'
	write(cmd)
	x=ser.readline()
	x=str(x.strip()).split("*")[0].split(',')[2:]
	regs=RREG[54][1]
	for i in range(len(regs)):
		print(regs[i],x[i])

	print("model number is: ",x)
	return x

def stop_async():
	"""" 
		stop asynchronously sent data so that a user can send commands and get responses back.
		without having to worry about other values being broadcasted by the sensor
		(for both uart channels)

	"""

	cmd1=b'$VNWRG,7,0,1*40\r'
	cmd2=b'$VNWRG,7,0,2*XX\r'
	write(cmd1)
	write(cmd2)

def model_name():
	# ser.flush()
	ser.reset_input_buffer()

	cmd=b'$VNRRG,1*9527\r'
	# print("reading angular rate\r")
	ser.write(cmd)
	x=ser.readline()
	x=str(x.strip()).split("*")[0].split(',')[-1]
	print("IMU data is : ",x)
	return x


# for i in range(50):
# 	if i <10:
# 		cmd=b'$VNRRG,0'+str(i).encode("ascii")+b"*XX\r"
# 	else:
# 		cmd=b'$VNRRG,'+str(i).encode("ascii")+b"*XX\r"
# 	write(cmd)
# 	# time.sleep(1)
# 	print(ser.readline().strip())








# stop_async()
# write(b'$VNRRG,04*XX')

get_imu_data()
# print(read_imu(ser))

model_name()
# 
ser.close()
