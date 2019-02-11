# a prototype for IMU data extraction
# uses default settings 
# connected to COM7, (change that for corresponding port)

Data={}
commands={}
cmd_model=b'$VNRRG,1*9527'
def write(ser,cmd):
	"""Write a command to the sensor """
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




## register number and format of data used
RREG={}
RREG.update({8:["yaw pitch roll",['Yaw','Pitch',"Roll"]]})
RREG.update({9:["Attitude Quaternion",["Quat[0]","Quat[1]","Quat[2]","Quat[3]"]]})
RREG.update({27:["Yaw,pitch,roll,Magnetic,Acceleration,and Angular Rates [YMR]",['Yaw','Pitch','Roll','MagX',"MagY","MagZ","AccelX","AccelY","AccelZ","GyroX","GyroY","GyroZ"]]})
RREG.update({15:["QMR",["Quat[0]","Quat[1]","Quat[2]","Quat[3]","MagX","MagY","MagZ","AccelX","AccelY","AccelZ","GyroX","GyroY","GyroZ"]]})
RREG.update({17:["Magnetic Measurements",["Magx","MagY","MagZ"]]})
RREG.update({18:["Acceleration Measurements",["AccelX","AccelY","AccelZ"]]})
RREG.update({19:["Compensated angular Rate Measurements",["GyroX","GyroY","GyroZ"]]})
RREG.update({20:["Magnetic,Acceleration, AND angular RATES",["Magx","MagY","MagZ","AccelX","AccelY","AccelZ","GyroX","GyroY","GyroZ"]]})
## configuration registers( read/write)
# VPE Basic Control
RREG.update({35:["Configuration registers",["enable","headingMode","filteringMode","tuningMode"]]})
#VPE basic Magnetometer Basic
RREG.update({36:["VPE Magnetometer Basic Tuning",['BaseTuningX',"BaseTuningY","BaseTuningZ","AdaptiveTuningx","AdaptiveTuningY","AdaptiveTuningZ"]]})
RREG.update({38:["VPE Acceleration Basic tuning",['BaseTuningX',"BaseTuningY","BaseTuningZ","AdaptiveTuningx","AdaptiveTuningY","AdaptiveTuningZ","AdaptiveFilteringX","AdaptiveFilteringY","AdaptiveFilteringZ"]]})
RREG.update({43:["Filter Startup Gyro Bias",["X-axis Gyro Bias Estimate","Y-axis Gyro Bias Estimate","Z-axis Gyro Bias Estimate"]]})
RREG.update({40:["VPE Gyro Basic Tuning",["VAngularWalkX","VAngularWalkY","VAngularWalkZ","BaseTuningX","BaseTuningY","BaseTuningZ","AdaptiveTuningX","AdaptiveTuningY","AdaptiveTuningZ"]]})
RREG.update({54:["IMU",["Magx","MagY","MagZ","AccelX","AccelY","AccelZ","GyroX","GyroY","GyroZ","Temp","Pressure"]]})
RREG.update({80:["Delta theta and velocity",["DeltaTime","DeltaThetaX","DeltaThetaY","DeltaThetaZ","DeltaVelocitx","DeltaVolocityY","DeltaVolocityZ"]]})

# hard/soft iron estimator //
RREG.update({44:["Magnetometer Calibration control",["HSIMode","HSIOutput","ConvergeRate"]]})
RREG.update({47:["Calculated Magnetometer Calibration",["C[0,0]","C[0,1]","C[0,2]","C[1,0]","C[1,1]","C[1,2]","C[2,0]","C[2,1]","C[2,2]","B[0]","B[1]","B[2]"]]})

RREG.update({51:["Velocity compansation control",["Mode","VelocityTuning","RateTuning"]]})
RREG.update({50:["Velocity Compansation Measurements",["VelocityX","VelocitY","VelocityZ"]]})
RREG.update({21:["Magnetic and gravity reference vectors",["MagRefX","MagRefY","MagRefZ","AccRefX","AccRefY","AccRefZ"]]})

RREG.update({83:["Reference Vector Configuration",["UseMagModel","UseGravityModel","Resv","Resv","RecalcThreshold","Year","Latitude","Longitude","Altitude"]]})
RREG.update({82:["Delta Theta and Delta velocity configuration",["IntegrationFrame","GyroCompensation","AccelCompensation","Reserved","Reserved"]]})
RREG.update({85:["IMU filtering Configuration",["MagWindowSize","AccelWindowSize","GryoWindowSize","TempWindowSize","PresWindowSize","MagFilterMode","AccelFilterMode","GyroFilterMode","TempFilterMode","PresFilterMode"]]})
RREG.update({26:["C[0,0]","C[0,1]",["C[0,1]","C[0,2]","C[1,0]","C[1,1]","C[1,2]","C[2,0]","C[2,1]","C[2,2]"]]})
RREG.update({84:["Gyro Compensation",["C[0,0]","C[0,1]","C[0,2]","C[1,0]","C[1,1]","C[1,2]","C[2,0]","C[2,1]","C[2,2]","B[0]","B[1]","B[2]"]]})
RREG.update({23:["Magnetic Compensation",["C[0,0]","C[0,1]","C[0,2]","C[1,0]","C[1,1]","C[1,2]","C[2,0]","C[2,1]","C[2,2]","B[0]","B[1]","B[2]"]]})
RREG.update({25:["Acceleration Compensation",["C[0,0]","C[0,1]","C[0,2]","C[1,0]","C[1,1]","C[1,2]","C[2,0]","C[2,1]","C[2,2]","B[0]","B[1]","B[2]"]]})


def get_imu_data(ser):
	ser.reset_input_buffer()
	cmd=b'$VNRRG,54*XX\r\n'
	write(ser,cmd)
	x=ser.readline()
	x=str(x.strip()).split("*")[0].split(',')[2:]
	regs=RREG[54][1]
	for i in range(len(regs)):
		print(regs[i],x[i])

	print("model number is: ",x)
	return x


def read_reg(ser,reg_number):
	ser.reset_input_buffer()
	cmd=b'$VNRRG,'+str(reg_number).encode("ascii")+b'*XX\r\n'
	write(ser,cmd)
	x=ser.readline()
	print(x)
	x=str(x.strip()).split("*")[0].split(',')[2:]
	regs=RREG[reg_number][1]
	for i in range(len(regs)):
		print(regs[i],x[i])

	print("contents: ",x)
	return x


def magneticDistubance(ser,value=0):
	cmd=b'$VNKMD,'+str(value).encode("ascii")+b'*47\r\n'
	write(ser,cmd)
	x=ser.readline()
	print(x)
def accelDisturbance(ser,value=0):
	cmd=b'$VNKAD'+str(value).encode("ascii")+b'*48\r\n'
	write(ser,cmd)
	x=ser.readline()
	print(x)

