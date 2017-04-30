import RPi.GPIO as GPIO

# Initialize
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
# Set all pins to output
for i in range(2,28):
	GPIO.setup(i, GPIO.OUT)
	GPIO.output(i, GPIO.LOW)

print('All output pins set to zero.')
