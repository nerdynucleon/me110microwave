import RPi.GPIO as GPIO
import time
import socket

GPIO.setwarnings(False)
TCP_IP = '107.170.224.107'
TCP_PORT = 443
BUFFER_SIZE = 1024

gpio_func = {
  'num0' : 24, 
  'num1' : 17, 
  'num2' : 4,  
  'num3' : 11, 
  'num4' : 6,  
  'num5' : 26, 
  'num6' : 10, 
  'num7' : 27, 
  'num8' : 14, 
  'num9' : 8,  
  'sec30orstart' : 16, 
  'reheat' : 19, 
  'kitchentimer' : 13, 
  'clearorstop' : 12, 
  'beverage' : 5, 
  'clock' : 7, 
  'frozen_vegetable' : 25, 
  'power' : 9, 
  'popcorn' : 23, 
  'timecook' : 22, 
  'potato' : 18, 
  'timedefrost' : 15, 
  'pizza' : 3, 
  'weightdefrost' : 2
}

def flip_GPIO(func):
    try:
      pin_num = gpio_func[func]
      GPIO.output(pin_num, GPIO.HIGH)
      time.sleep(0.5)
      GPIO.output(pin_num, GPIO.LOW)	
    except Exception as err:
      print(err.message)

# Initialize
GPIO.setmode(GPIO.BCM)
# Set all pins to output and low
for i in range(2,28):
	GPIO.setup(i, GPIO.OUT)
	GPIO.output(i, GPIO.LOW)
# Open Socket to Server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

while(1):
	try:
		s.connect((TCP_IP, TCP_PORT))
		break
    	except:
        	attempts = 1
while(1):
	data = s.recv(BUFFER_SIZE)
	print "recv:", data
  for cmd in data.split('|'):
    flip_GPIO(cmd)

s.close()
