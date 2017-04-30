import RPi.GPIO as GPIO

# Initialize
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
# Set all pins to output
for i in range(2,28):
	GPIO.setup(i, GPIO.OUT)
	GPIO.output(i, GPIO.LOW)

print('All output pins set to zero.')

# Pull new code from repository
import socket
import os

while(True):
	try:
		socket.setdefaulttimeout(3)
		socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(("8.8.8.8", 53))
		os.system('git --git-dir=/home/pi/me110microwave/.git pull')
		break
	except Exception as err:
		print(ex.message)
