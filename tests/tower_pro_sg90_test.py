#!/usr/bin/python

import sys
sys.path.append("/home/pi/shared")

from libraries.Adafruit_PWM_Servo_Driver import PWM
from pwm_objects.tower_pro_sg90 import TowerProSG90
import time


class TowerProSG90Test():

    ADDRESS = 0x40
    FREQUENCY = 50
    CHANNEL = 7

    def __init__(self, inverted=False):
        self.pwm = None
        self.pwm = PWM(self.ADDRESS)
        self.pwm.setPWMFreq(self.FREQUENCY)
        self.servo = TowerProSG90(self.pwm, self.CHANNEL, inverted)

    def test_angle(self, angle):
        pwm_value = self.servo.set_angle(angle)
        print('PWM right: {} PWM middle: {} PWM left: {} PWM value: {} Angle: {}'.format(self.servo.right_value,
                                                                                         self.servo.middle_value,
                                                                                         self.servo.left_value,
                                                                                         pwm_value, angle))

    def test_angle_automatic(self):
        test_values = [90, 45, 0, -45, -90]

        for angle in test_values:
            self.test_angle(angle)
            time.sleep(2)

    def test_angle_incremental(self):
        print('')
        for angle in range(-90, 91):
            self.servo.set_angle(angle)

            if angle % 10 == 0:
                print('Angle: {}'.format(angle))

            time.sleep(0.01)

    def test_angle_interactive(self):
        while True:
            angle = int(input('Angle: '))
            self.test_angle(angle)


print('Normal:\n')
tp_test = TowerProSG90Test()

tp_test.test_angle_automatic()
tp_test.test_angle_incremental()

print('\nInverted:\n')
tp_test = TowerProSG90Test(True)

print('Automatic mode:\n')
tp_test.test_angle_automatic()
tp_test.test_angle_incremental()
print('\nInteractive mode:\n')
tp_test.test_angle_interactive()