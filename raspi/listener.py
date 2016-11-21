#!/usr/bin/python

import sys, getopt, datetime, serial

dataFilePath = 'data.csv'

try:
	opts, args = getopt.getopt(sys.argv[1:], "t:", ["tty="])
except getopt.GetoptError:
	print 'listener.py -t /dev/ttyX'
	sys.exit(2)
for opt, arg in opts:
	if opt == '-t' or opt == '--tty':
		tty = arg

if tty:
	ser = serial.Serial(tty, 9600)
	while 1 :
		data = ser.readline() # read moisture level and temperature
		now = datetime.datetime.today()
		nowString = now.strftime('%m/%d/%Y %H:%M:%S')
		dataFile = open(dataFilePath, 'a')
		dataFile.write(nowString + ', ' + str(data))
		dataFile.close()




