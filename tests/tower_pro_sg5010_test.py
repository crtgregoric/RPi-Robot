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
    CHANNEL_LEFT = 0
    CHANNEL_RIGHT = 15

    def __init__(self, position=MotorPosition.LEFT):
        self.pwm = PWM(self.ADDRESS)
        self.pwm.setPWMFreq(self.FREQUENCY)

        if position == MotorPosition.LEFT:
            self.servo = TowerProSG5010(self.pwm, self.CHANNEL_LEFT, position)
        else:
            self.servo = TowerProSG5010(self.pwm, self.CHANNEL_RIGHT, position)

    def test_speed(self, speed):
        pwm_value = self.servo.set_speed(speed)
        print('PWM back: {} PWM stop: {} PWM forward: {} PWM value: {} Speed: {}'.format(self.servo.backwards_value,
                                                                                         self.servo.stop_value,
                                                                                         self.servo.forward_value,
                                                                                         pwm_value, speed))

    def test_speed_automatic(self):
        test_values = [100, 50, 0, -50, -100]

        for speed in test_values:
            self.test_speed(speed)
            time.sleep(4)

    def test_speed_incremental(self):
        print('')
        for speed in range(101):
            self.servo.set_speed(speed)

            if speed % 10 == 0:
                print('Speed : {}'.format(speed))

            time.sleep(0.1)

    def test_speed_interactive(self):
        while True:
            speed = int(input('Speed: '))
            self.test_speed(speed)


print('Left - normal:\n')
tp_test = TowerProSG5010Test()

tp_test.test_speed_automatic()
tp_test.test_speed_incremental()

time.sleep(2)

print('\nRight - inverted:\n')
tp_test = TowerProSG5010Test(MotorPosition.RIGHT)

print('Automatic mode:\n')
tp_test.test_speed_automatic()
tp_test.test_speed_incremental()
print('\nInteractive mode:\n')
tp_test.test_speed_interactive()