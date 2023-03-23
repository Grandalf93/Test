import RPi.GPIO as GPIO
import time


#GPIO Setup
GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.OUT)#IN A
GPIO.setup(11, GPIO.OUT)#EN A
GPIO.setup(12, GPIO.OUT) #PWM motor
GPIO.setup(13, GPIO.OUT)#IN B

p = GPIO.PWM(12, 50)
p.start(0)

GPIO.output(7, True)
GPIO.output(11,True)
GPIO.output(13, False)

try:
    while True:
        for dc in range(0,101,5):
            p.ChangeDutyCycle(dc)
            print(dc)
            time.sleep(1)
        for dc in range(100, -1, -5):
            p.ChangeDutyCycle(dc)
            print(dc)
            time.sleep(1)
except KeyboardInterrupt:
    pass
p.stop()
GPIO.cleanup()

