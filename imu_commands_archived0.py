# a prototype for IMU data extraction
# uses default settings 
# connected to COM7, (change that for corresponding port)

import serial
import time
Data={}
commands={}
cmd_model=b'$VNRRG,1*9527'
def write(ser,cmd):
	ser.write(cmd)

def get_serial_number(ser):
	ser.reset_input_buffer()
	cmd=b'$VNRRG,03*XX\r\n'
	write(ser,cmd)
	x=ser.readline()
	x=str(x.strip()).split("*")[0].split(',')[-1]
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

def model_name(ser):
	# ser.flush()
	cmd=b'$VNRRG,1*9527\r'
	# print("reading angular rate\r")
	ser.write(cmd)
	x=ser.readline()
	x=str(x.strip()).split("*")[0].split(',')[-1]
	print("model name: ",x)
	return x


