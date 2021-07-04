import time
import uping
import os

if __name__=="__main__":
	import network
	connection = network.WLAN(network.STA_IF)
	connection.active(True)
	connection.scan()                             # Scan for available access points
	connection.connect("HenryDM", "3045558165") # Connect to an AP
	connection.isconnected()                      # Check for successful connection
	avg=0
	count=20
	add = 0
	for x in range(count):
		tic = time.ticks_ms()
		trans,reciv = uping.ping("8.8.8.8", size=64)
		toc = time.ticks_ms()-tic
		if trans==reciv:
			add = add+1
			avg=avg+toc
	avg = avg/add
	print(avg)


	
