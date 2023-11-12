import RPi.GPIO as GPIO
import time

# Define GPIO pins for Step and Direction
STEP_PIN = 23
DIR_PIN = 22


EN_pin = 24 # enable pin (LOW to enable)

MS1 = 25
MS2 = 8

# Set the GPIO mode and setup the pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(STEP_PIN, GPIO.OUT)
GPIO.setup(DIR_PIN, GPIO.OUT)
GPIO.setup(EN_pin,GPIO.OUT) # set enable pin as output

GPIO.setup(MS1, GPIO.OUT)
GPIO.setup(MS2, GPIO.OUT)

# Function to move the stepper motor
def move_stepper(steps, delay=0.001):

    GPIO.output(MS1, GPIO.LOW)
    GPIO.output(MS2, GPIO.LOW)

    GPIO.output(EN_pin,GPIO.LOW) # pull enable to low to enable motor
    GPIO.output(DIR_PIN, GPIO.HIGH)  # Set the direction (HIGH for clockwise, LOW for counterclockwise)

    for _ in range(steps):
        GPIO.output(STEP_PIN, GPIO.HIGH)
        time.sleep(delay)
        GPIO.output(STEP_PIN, GPIO.LOW)
        time.sleep(delay)

# Move the stepper motor 200 steps (adjust as needed)
move_stepper(200*8)

# Cleanup GPIO
GPIO.cleanup()