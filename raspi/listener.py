#!/usr/bin/python

import sys, getopt, datetime, serial

from threading import Timer
from astral import Astral
from pytz import timezone
from Adafruit_IO import *

aio = Client('xxxx')

dailyWateringHour = 9

localTz = timezone('US/Mountain')
city_name = 'Denver'

dataFilePath = 'data.csv'

a = Astral()
a.solar_depression = 'civil'

city = a[city_name]

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

	# Define callback functions which will be called when certain events happen.

	def stopWater():
		ser.write('W0')
		aio.send('Garden-WaterSwitch', 'OFF')
		print('Water stopped')

	def start9amWatering():
		# Water only for 45 seconds every day
		aio.send('Garden-WaterSwitch', 'ON')
		ser.write('W1')
		t9amStop = Timer(45, stopWater)
		t9amStop.start()
		setup9amWatering() # Schedule for tomorrow!
		print('Water started')

	def setup9amWatering():
		now = datetime.datetime.now(localTz)
		if (now.hour < 9):
			# start timer for today
			print('Water today at 9am')
			futureTime = datetime.datetime(now.year, now.month, now.day, dailyWateringHour, 0, 0, 0, localTz)
		else:
			# start timer for tomorrow
			print('Water tomorrow at 9am')
			delta = now + datetime.timedelta(days=1)
			futureTime = datetime.datetime(delta.year, delta.month, delta.day, dailyWateringHour, 0, 0, 0, localTz)
		difference = futureTime - now
		t9am = Timer(difference.total_seconds(), start9amWatering)
		t9am.start()

	def stopNightLight():
		ser.write('L0')
		aio.send('Garden-LightSwitch', 'OFF')
		setupSunsetLighting() # Schedule for tomorrow

	def startNightLight():
		ser.write('L1')
		aio.send('Garden-LightSwitch', 'ON')
		now = datetime.datetime.now(localTz)
		sun = city.sun(date=now, local=True)
		if (now > sun['sunset']):
			tomorrow = now + datetime.timedelta(days=1)
			sun = city.sun(date=tomorrow, local=True)
			print('Schedule night light for tomorrow')
		else:
			print('Schedule night light for later today')
		difference = sun['sunrise'] - now
		tNightLightOff = Timer(difference.total_seconds(), stopNightLight)
		tNightLightOff.start()

	def setupSunsetLighting(dateToUse):
		now = datetime.datetime.now(localTz)
		sun = city.sun(date=now, local=True)
		if (sun['sunset'] < now):
			# this already happened, so let's schedule for tomorrow
			tomorrow = now + datetime.timedelta(days=1)
			sun = city.sun(date=tomorrow, local=True)
		difference = sun['sunset'] - now
		tNightLight = Timer(difference.total_seconds(), startNightLight)
		tNightLight.start()

	def setupLighting():
		now = datetime.datetime.now(localTz)
		sun = city.sun(date=now, local=True)
		tomorrow = now + datetime.timedelta(days=1)
		if (now > sun['sunset'] or now < sun['sunrise']):
			# It's dark right now
			print('It is dark now - turn light on')
			startNightLight()
		if (now < sun['sunset'] and now > sun['sunrise']):
			# It's light out
			print('It is light now - turn light off and schedule turn on time')
			stopNightLight()
			setupSunsetLighting()

	def connected(client):
		# Connected function will be called when the client is connected to Adafruit IO.
		# This is a good place to subscribe to feed changes.  The client parameter
		# passed to this function is the Adafruit IO MQTT client so you can make
		# calls against it easily.
		print 'Connected to Adafruit IO!  Listening for Light and Water Switch changes...'
		# Subscribe to changes on a feed named DemoFeed.
		client.subscribe('Garden-LightSwitch')
		client.subscribe('Garden-WaterSwitch')

	def disconnected(client):
		# Disconnected function will be called when the client disconnects.
		print 'Disconnected from Adafruit IO!'
		#if (client.disconnect_reason != MQTT_ERR_SUCCESS):
		print 'Client disconnected, reconnecting'
		client.connect()
		#else:
		#	sys.exit(1)

	def message(client, feed_id, payload):
		# Message function will be called when a subscribed feed has a new value.
		# The feed_id parameter identifies the feed, and the payload parameter has
		# the new value.
		if (feed_id == 'Garden-LightSwitch'):
			if (payload == 'ON'):
				print 'Turn light on'
				print ser.write('L1')
			else:
				print 'Turn light off'
				print ser.write('L0')
		if (feed_id == 'Garden-WaterSwitch'):
			if (payload == 'ON'):
				ser.write('W1')
				t = Timer(60, stopWater)
				t.start()
			else:
				ser.write('W0')
		print 'Feed {0} received new value: {1}'.format(feed_id, payload)

	# Create an MQTT client instance.
	client = MQTTClient(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

	# Setup the callback functions defined above.
	client.on_connect    = connected
	client.on_disconnect = disconnected
	client.on_message    = message

	# Connect to the Adafruit IO server.
	client.connect()

	# Now the program needs to use a client loop function to ensure messages are
	# sent and received.  There are a few options for driving the message loop,
	# depending on what your program needs to do.

	# The first option is to run a thread in the background so you can continue
	# doing things in your program.
	client.loop_background()

	setup9amWatering()
	setupLighting()
	while 1 :
		data = ser.readline() # read moisture level and temperature
		now = datetime.datetime.now(localTz)
		nowString = now.strftime('%m/%d/%Y %H:%M:%S')
		dataFile = open(dataFilePath, 'a')
		outputString = nowString + ', ' + str(data)
		dataFile.write(outputString)
		dataFile.close()
		print outputString
		dateString, soil1, soil2, temp, darkness = outputString.split(', ')
		soil1 = int(soil1)
		soil2 = int(soil2)
		temp = float(temp)
		darkness = float(darkness.strip())
		try:
			aio.send('Garden-Soil1', soil1)
			aio.send('Garden-Soil2', soil2)
			aio.send('Garden-Temp', temp)
			aio.send('Garden-Darkness', darkness)
		except:
			continue
