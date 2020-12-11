#!/usr/bin/env python
from ki import SerialDataGateway

if __name__ == '__main__':
	speed_message = 1
	print speed_message
	ser = SerialDataGateway()
	ser.Start()
	ser.Write(str(speed_message))
	ser.Stop()
