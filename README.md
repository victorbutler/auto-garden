# Auto Garden #
Adventures in automating food growth

## Phase 1 ##
Using a Soil Moisture sensor, take meaningful measurements of soil moisture content to determine when soil is *Too Dry* and needs *Watering*.

### Status ###
**11/19/2016**: We can take measurements and track data over time.

## How? ##
1. An Arduino reads the sensor data every 60 seconds and sends that data to a Raspberry Pi over the Serial USB.
2. The Raspberry Pi records that data along with the date and organizes output into a CSV file.

## Setup ##
1. There is a [PiBakery](http://www.pibakery.org) recipe included that you can use to get your Raspberry Pi set up. Change the WiFi SSID and password to yours.
2. Program the Arduino with the included Sketch (using the [Arduino software](https://www.arduino.cc/en/Main/Software)). It uses A0 as the ADC input for the sensor.
3. Wire up the sensor using the +5v, GND and A0 pins on the board.

## Links ##
* Schematic: https://circuits.io/circuits/3426362-auto-garden-v1-0