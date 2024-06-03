from constants import *
import serial

comPort = input("COM")
ser = serial.Serial(
   port='COM' + comPort,
   baudrate=3000000, #3 mil by def
   parity=serial.PARITY_NONE,
   stopbits=serial.STOPBITS_ONE,
   bytesize=serial.EIGHTBITS
)

senddata = [0 for i in range(7)]
senddata[0] = 0x0F

def TransferData(ubtnFlag, ubtnData,deltaX, deltaY):
	global senddata
	global ser    
	mouseevent = 1

	ud = ubtnData
	ulButtons = ubtnFlag
	if ud == SCROLL_UP or ud == SCROLL_DOWN:
		print("wheel is clicked")
		if ud == 120:
			ud = 1
		else :
			ud = -1 

		senddata[1] = 0x02
		senddata[2] = (ud >> 8) & 0xFF
		senddata[3] = (ud ) & 0xFF
		senddata[4] = 0
		senddata[5] = 0
		crcSum = CalculateCRC_1(senddata[:-1])  
		senddata[6] = (crcSum ) & 0xFF

	elif ulButtons == LEFTBUTTON_DOWN or ulButtons == LEFTBUTTON_UP or ulButtons == RIGHTBUTTON_DOWN or ulButtons == RIGHTBUTTON_UP or ulButtons == FORWARDBUTTON_DOWN or ulButtons == FORWARDBUTTON_UP or ulButtons == BACKBUTTON_DOWN or ulButtons == BACKBUTTON_UP:
		print("mouse clicked")
		buttonEvent = 0
		# We don't have a if statement for Right because we assume it is + 0 for both up and down
		if ulButtons == LEFTBUTTON_DOWN or ulButtons == LEFTBUTTON_UP:
			buttonEvent = buttonEvent + 1
		
		if ulButtons == LEFTBUTTON_DOWN or ulButtons == RIGHTBUTTON_DOWN:
			# When a mouse button is pressed down, its event code is shifted by two positions to the right. 
			# This results in a value of 2 for a right click push and a value of 3 for a left click push. 
			# When a mouse button is released, its event code is not shifted, resulting in a value of 0 for a 
			# right click release and a value of 1 for a left click release.
			buttonEvent = buttonEvent + 2

		if ulButtons == BACKBUTTON_DOWN or ulButtons == BACKBUTTON_UP:
			#print("side button clicked")
			buttonEvent = buttonEvent + 4
		if ulButtons == FORWARDBUTTON_DOWN or ulButtons == FORWARDBUTTON_UP:
			#print("side button clicked")
			buttonEvent = buttonEvent + 5


		#print("BUTTON EVENT = " + str(buttonEvent))
		senddata[1] = 0x01 + (buttonEvent << 6)
		#print(senddata[1] >> 6)
		senddata[2] = 0x0
		senddata[3] = 0x0
		senddata[4] = 0x0
		senddata[5] = 0x0

	elif ud == 0 and ulButtons == 0:

		print("mouse is moving") 
		senddata[1] = 0x03
		#print(senddata[1] >> 6)
		senddata[2] = (deltaX >> 8) & 0xFF
		senddata[3] = (deltaX ) & 0xFF
		senddata[4] = (deltaY >> 8) & 0xFF
		senddata[5] = (deltaY ) & 0xFF
	else:
		print('other event') 
		mouseevent = 0

	if mouseevent == 1:
		crcSum = CalculateCRC_1(senddata[:-1])  
		senddata[6] = (crcSum ) & 0xFF      
		print(senddata)
		ser.write(senddata)

def CalculateCRC_1(data):
	crc = 0xFF
	for pos in data:
		crc ^= pos
	return crc