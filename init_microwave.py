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
import os

while(True):
	resp = os.system("ping -c 1 8.8.8.8")
	if resp == 0:	
		os.system('git --git-dir=/home/pi/me110microwave/.git pull')
		break
	else:
		print('no connection to google')
