#!/usr/bin/python

from libraries.Adafruit_PWM_Servo_Driver import PWM
from pwm_objects.tower_pro_sg90 import TowerProSG90
import time


class TowerProSG90Test():

    ADDRESS = 0x40
    FREQUENCY = 50
    CHANNEL = 7

    def __init__(self, inverted=False):
        self.pwm = PWM(self.ADDRESS)
        self.pwm.setPWMFreq(self.FREQUENCY)
        self.servo = TowerProSG90(self.pwm, self.CHANNEL, inverted)

    def test_angle(self, angle):
        pwm_value = self.servo.set_angle(angle)
        print('PWM right: {} PWM middle: {} PWM left: {} PWM value: {}'.format(self.servo.RIGHT_VALUE,
                                                                               self.servo.MIDDLE_VALUE,
                                                                               self.servo.LEFT_VALUE, pwm_value))

    def test_angle_automatic(self):
        test_values = [90, 45, 0, -45, -90]

        for angle in test_values:
            self.test_angle(angle)
            time.sleep(2)

    def test_angle_interactive(self):
        angle = int(input('Angle: '))
        self.test_angle(angle)


print('\nNormal:\n')

tp_test = TowerProSG90Test()

tp_test.test_angle_automatic()

print('\nInverted:\n')

tp_test = TowerProSG90Test(True)

print('\nAutomatic mode:\n')
tp_test.test_angle_automatic()

print('\nInteractive mode:\n')
tp_test.test_angle_interactive()