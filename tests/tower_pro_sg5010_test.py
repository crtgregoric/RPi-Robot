#!/usr/bin/python

import sys
sys.path.append("/home/pi/shared")

from libraries.Adafruit_PWM_Servo_Driver import PWM
from pwm_objects.tower_pro_sg5010 import TowerProSG5010
from helpers.motor_position import MotorPosition
import time


class TowerProSG5010Test():

    ADDRESS = 0x40
    FREQUENCY = 50
    CHANNEL = 0

    def __init__(self, position=MotorPosition.RIGHT):
        self.pwm = PWM(self.ADDRESS)
        self.pwm.setPWMFreq(self.FREQUENCY)
        self.servo = TowerProSG5010(self.pwm, self.CHANNEL, position)

    def test_speed(self, speed):
        pwm_value = self.servo.set_speed(speed)
        print('PWM right: {} PWM middle: {} PWM left: {} PWM value: {} Speed: {}'.format(self.servo.BACKWARDS_VALUE,
                                                                                         self.servo.STOP_VALUE,
                                                                                         self.servo.FORWARD_VALUE,
                                                                                         pwm_value, speed))

    def test_speed_automatic(self):
        test_values = [100, 50, 0, -50, -100]

        for speed in test_values:
            self.test_speed(speed)
            time.sleep(4)

    def test_speed_incremental(self):
        for speed in range(101):
            self.servo.set_speed(speed)

            if speed % 10 == 0:
                print('Speed :'.format(speed))

            time.sleep(0.001)

    def test_speed_interactive(self):
        while True:
            speed = int(input('Speed: '))
            self.test_speed(speed)


print('\nRight - normal:\n')

tp_test = TowerProSG5010Test()

tp_test.test_speed_automatic()

print('\nLeft - inverted:\n')

tp_test = TowerProSG5010Test(MotorPosition.LEFT)

print('\nAutomatic mode:\n')
tp_test.test_speed_automatic()

print('\nInteractive mode:\n')
tp_test.test_speed_interactive()