import serial
import time
import string
import sys
import getopt
import os
from sys import exit
list1=['010D','010C','0105','0133','010F','0108','0106','010B','0110','015B','015E','0146','0131','0104']  #Creates a list of the PID's to be checked
list2= list()  #Creates a second list in the supported PID's are stacked up

#time.sleep(1)
port = serial.Serial("/dev/ttyUSB0", baudrate=9600, timeout=1.0,bytesize=8,stopbits=1)
port.flushInput()
port.flushOutput()
"for gps initialization----"
"""
serial_port = "/dev/ttyACM0"
serial_baud = 4800
gps = serial.Serial(serial_port, serial_baud, timeout=1)"""

port.write("ATZ\r")

def flush():
    port.flushInput()
    port.flushOutput()
    port.flush()

def one(rcv): # Calculating the decimal value of 1 byte hexadecimal numbers
    r=rcv.split('\r',1)
    data=r[1]
    v = data[6:-3] # A substring from index 6 to -3 including both - Python indexing start from 0
    print v
    vspeed=int(v,16)   
    return vspeed
    
def two(rcv): #Calculating the decimal value of 2 bytes hexadecimal numbers
    r=rcv.split('\r',1)
    data=r[1]
    v=data[6:-3]
    a=int(v[0:2],16)
    b=int(v[3:5],16)
    return {'A':a,'B':b}

def support():
    flush()
    port.write('0111\r')
    rcv=port.readline()
    print repr(rcv)


def no_value(data):
    if data[0:-3] == 'NO DATA':
        return 0  
    else:
        return 1

		
def nodtc(rcv):
    flush()
    rcv = rcv[0:-4]
    if rcv == "NO DATA":
        return 0
    else:
        return 1
        

def DTC_decrypt():
    flush()
    port.write("03\r")
    rcv = port.readline()
    v=rcv.split("\r",1)
    check = nodtc(v)
    if check == "0":
        print("No Fault Detected")
    else:            
        v=v[1][6:-4]# NEED TO check - v[1][6:-3]?
        f1=v[0:2]    
        f3=v[3:4]
        f4=v[4:5]
    
        f1 = (bin(int(str(f1),16))[2:]).zfill(8) #bin(int(str function to get a binary string, [2:] to crop from indexing2
    
     # NOW finding the type of fault code : P,C,B,U - 1st DTC
        x = f1[0:2] 
        if (x == "00"): 
            a = "P"
        elif (x == "01"):
            a = "C" 
        elif (x == "10"):
            a = "B"
        else :
            a = "U"

        y = f1[2:4]
        b = int(y,2)

        z = f1[4:8]
        c = int(z,2)

        dtc = a+repr(b)+repr(c)+f3+f4
        print("DTC Code is "+dtc)

def check_pid():             #Checking for the supported PID's in the car
    count=0
    for index in range(len(list1)): #Scanning through the list of PID's
        flush()
        port.write(list1[intex]+'\r')
        rcv = port.readline()
        x=no_value(rcv)
        if(x==1):
            list2[count]=list1[index]  #if the returned value is 1 then the PID is supported and it is then copied to the second list
            count=count+1

def CallSupportedPID(): #in this function as the names are changed to the corrosponding pid's the names with the suported pid's are called with the names
    for item in list:
        possibles = globals().copy()
        possibles.update(locals())
        method = possibles.get(item)()    
        if not method:
             raise Exception("Method %s not implemented" % method_name)
        method()

def 010D():
    flush()
    port.write("010D\r")
    rcv = port.readline()
    x=no_value(rcv)
    print ("x for speed is " + repr(x))
    
    print (repr(rcv))
#    print("Vehicle Speed\n"+repr(rcv))
    if (x==1)
        vspeed = one(rcv)
        print("\nVehicle Speed: " + repr(vspeed)+"Km/H.")
        #f.write("Vehicle Speed -" + repr(vspeed)+"Km/H;")
        return vspeed
    
 
def 010C():
    flush()
    port.write("010C\r")
    rcv = port.readline()
    x=no_value(rcv)
    print("X for rpm is : " + repr(x))
    if (x==1)
        print("\n"+ repr(rcv))
        r=two(rcv)
        a=r['A']; b=r['B']
        rpm=(a*256+b)/4   
        print("\nEngine RPM:" + repr(rpm) +"rpm.")
    #f.write("Engine RPM - " + repr(rpm)+";")
        return rpm    
    #print a
    #print b
    
def 0105():
    flush()
    port.write("0105\r")
    rcv = port.readline()
    x=no_value(rcv)
    print("X for cool temp is : " + repr(x))
    if (x==1)
#    print rcv
        tmp=one(rcv)
        t=tmp-40
        print("\nEngine Coolant Temp.:"+ repr(t)+" degree Celsius.")
    #f.write("Engine Coolant Temp-" + repr(t)+";")
        return t
    
def 0133():
    flush()
    port.write("0133\r")
    rcv=port.readline()
    tmp=one(rcv)
    print("\n Barometric Pressure:" + repr(tmp)+" Kpa")
    p= repr(tmp)
    return p
    #f.write("Barometric Pressure-"+ repr(tmp)+";")

def 010F():
    flush()
    port.write("010F\r")
    rcv = port.readline()
    tmp = one(rcv)
    tmp = tmp - 40
    print("\nIntake Air Temp: "+repr(tmp)+" degree Celsius.")
    return tmp
	#f.write("Intake Air Temp - "+repr(tmp)+";")
    
def 0111():
    flush()
    port.write("0111\r")
    rcv = port.readline()
    x=no_value(rcv)
    print("X for throtle is : " + repr(x))
        if (x==1)
        thr=one(rcv)
        thr=thr*100/255
        print("\nThrottle position:"+repr(thr)+" %.")
        return thr
	#f.write("Throttle position - "+repr(thr)+"%;")
     
def 011F():
    flush()
    port.write("011F\r")
    rcv = port.readline()
    rt=two(rcv)
    a=rt['A']; b=rt['B']
    time = a*256 + b
    print("\nRun Time since Engine start: "+repr(time)+" seconds")
    repr(time)
    return time
    #return time
	#f.write("Run Time since Engine start - "+repr(time)+"seconds;")

def 0104():
    flush()
    port.write("0104\r")
    rcv = port.readline()
    x=no_value(rcv)
    print("X for eng load is : " + repr(x))
    if (x==1)
        lv=one(rcv)
        elv=lv*100/255
        print("\nCalculated Engine Load Value: "+repr(elv)+" %")
        eng = repr(elv)
        return eng
    #f.write("Calculated Engine Load Value - "+repr(elv)+"%;")

def 0131(): #Distance travelled since codes cleared
    flush()
    port.write("0131\r")
    rcv=port.readline()
    dis=two(rcv)
    a=dis['A']; b=dis['B']
    dt=a*256 + b
    print("\nDistance travelled since codes cleared: "+repr(dt)+" Km" )
    return dt
	#f.write("Distance travelled since codes cleared - "+repr(dt)+"Km;" )

def 0146():
    flush()
    port.write("0146\r")
    rcv = port.readline()
    a=one(rcv)
    a = a - 40
    print("\nAmbient Air Temp: "+repr(a)+" degree Celsius")
    return a
	#Does not humidity and other parameters of the environment

def 015E():
    flush()
    port.write("015E\r")
    rcv=port.readline()
    v=two(rcv)
    a=v['A']; b=v['B']
    rate = (a*256+b)*(0.05)
    #print("\nEngine Fuel Rate: "+repr(rate)+" L/h")
    

def 015B():
    flush()
    port.write("015B\r")
    rcv = port.readline()
    v=one(rcv)
    time = v*100/255
    print("\nHybrid battery remaining life: "+repr(time)+" %")
    return time
	#print("\nHybrid battery remaining life: "+repr(time)+" %")
    

def 0110():# maf sensor supported
    flush()
    vspeed = speed()
    flush()
    port.write("0110\r")
    rcv = port.readline()
    f=two(rcv)
    a = f['A']; b = f['B']
    maf = (a*256 + b)/100
    mpg = (7.107*vspeed)/maf
    #print ("\nInstantaneous fuel economy is: "+repr(mpg)+" MPG")
    

def 010B():
    flush()
    port.write("010B\r")
    rcv = port.readline()
    #print rcv
    imap = one(rcv)
    #print imap
    maf = (imap)*(0.85)*4*(28.97)/(120*8.314)
    #print maf
    vspeed = speed()
    mpg = (7.107*vspeed)/maf    
    #print (repr(mpg)+";")
    return mpg
        
def 0106():
    flush()
    port.write("0106\r")
    rcv = port.readline()
    st = one(rcv)
    st = ((st-128)/128)*100
    print ("\nShort term fuel bank: "+repr(st)+" %")
    return st
	#f.write("Short term fuel bank - "+repr(st)+"%;")

def 0108():
    flush()
    port.write("0108\r")
    rcv = port.readline()
    lt = one(rcv)
    lt = ((lt-128)/128)*100
    print ("\nLong term fuel bank: "+repr(lt)+" %")
    return lt
	#f.write("Long term fuel bank - "+repr(lt)+"%;")

def fuel_consum():
    flush()
    rp = rpm()
    th = throttle()

try:
    speed()
    rpm()
    cooltemp()    #dummy
    intaketemp()
    throttle()
    pressure()
    engineload()
    latitude()

"""<<<<------------GPS CODE-------------->>>>>
def latitude():
	# defaults
	print "Serving data from %s (%d baud) for latitude" % (serial_port, serial_baud)
	latitude = 0
        longitude = 0
	line = gps.readline()
	print line
	datablock = line.split(',')
	print datablock
	
	if line[0:6] == '$GPGGA':
		print "Hello"
		latitude_in = string.atof(datablock[2])
                longitude_in = string.atof(datablock[4])
		if datablock[3] == 'S':
			latitude_in = -latitude_in
			
                if datablock[5] == 'W':
			longitude_in = -longitude_in

		longitude_degrees = int(longitude_in/100)
		longitude_minutes = longitude_in - longitude_degrees*100
		longitude = longitude_degrees + (longitude_minutes/60)
		latitude_degrees = int(latitude_in/100)
		latitude_minutes = latitude_in - latitude_degrees*100
		latitude = latitude_degrees + (latitude_minutes/60)
		
		print "Latitude is %s" % (latitude)
                print "Longitude is %s" % (longitude)
	return {'Latitude':latitude,'Longitude' : longitude}

----------------------------------->>>>>>>>"""
    
    
except KeyboardInterrupt:	
	exit(0)	
