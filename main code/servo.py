# This example moves a servo its full range (180 degrees by default) and then back.

from board import SCL, SDA
import busio
from lcd import *
from net import *
import time
import json
# Import the PCA9685 module.
from adafruit_pca9685 import PCA9685

# This example also relies on the Adafruit motor library available here:
# https://github.com/adafruit/Adafruit_CircuitPython_Motor
from adafruit_motor import servo

i2c = busio.I2C(SCL, SDA)

# Create a simple PCA9685 class instance.
pca = PCA9685(i2c)
pca.frequency = 50
# lcd_print(0,0,5,"test")
# To get the full range of the servo you will likely need to adjust the min_pulse and max_pulse to
# match the stall points of the servo.
# This is an example for the Sub-micro servo: https://www.adafruit.com/product/2201
# servo7 = servo.Servo(pca.channels[7], min_pulse=580, max_pulse=2480)
# This is an example for the Micro Servo - High Powered, High Torque Metal Gear:
#   https://www.adafruit.com/product/2307
# servo7 = servo.Servo(pca.channels[7], min_pulse=600, max_pulse=2400)
# This is an example for the Standard servo - TowerPro SG-5010 - 5010:
#   https://www.adafruit.com/product/155
# servo7 = servo.Servo(pca.channels[7], min_pulse=600, max_pulse=2500)
# This is an example for the Analog Feedback Servo: https://www.adafruit.com/product/1404
# servo7 = servo.Servo(pca.channels[7], min_pulse=600, max_pulse=2600)

# The pulse range is 1000 - 2000 by default.


def Servo_move_X(Id, Direction):
    servo = servo.Servo(pca.channels[Id])
    try:
        if Direction == "L":
            # 90度置中點
            for i in range(0, 90):
                servo.angle = 90 - i
        if Direction == "R":
            for i in range(90, 180):
                servo.angle = i
    except ValueError:
        print("Angle out of range")
    finally:
        pca.deinit()


def Servo_move_Y(Id, Direction):
    servo = servo.Servo(pca.channels[Id])
    try:
        if Direction == "D":
            # 90度置中點
            for i in range(0, 90):
                servo.angle = 90 - i
        if Direction == "U":
            for i in range(90, 180):
                servo.angle = i
    except ValueError:
        print("Angle out of range")
    finally:
        pca.deinit()
        
def Servo_move(Direction):
    servox = servo.Servo(pca.channels[0])
    servoy = servo.Servo(pca.channels[1])
    try:
        if Direction == "L":
            # 90度置中點
            for i in range(0, 90):
                servox.angle = 90 - i
        if Direction == "R":
            for i in range(90, 180):
                servox.angle = i
        if Direction == "D":
            for i in range(0, 90):
                servoy.angle = 90 - i
        if Direction == "U":
            for i in range(90, 180):
                servoy.angle = i
    except ValueError:
        print("Angle out of range")
    finally:
        pca.deinit()

def Servo_move_test(Direction):
    servox = servo.Servo(pca.channels[0])
    servoy = servo.Servo(pca.channels[1])
    try:
        Direction=eval(Direction)
        #print (Direction[0])
        #print (type(Direction[0]))
        servox.angle = int(Direction[0]['x_angle'])
        print (Direction[0]['x_angle'])
        servoy.angle = int(Direction[0]['y_angle'])
        print (Direction[0]['y_angle'])
    except ValueError:
        print("Angle out of range")

if __name__ == "__main__":
    while True:
        control_command=control('http://192.168.0.3:8000/api/control_output')
        if control_command:
            Servo_move_test(control_command)
        time.sleep(1)