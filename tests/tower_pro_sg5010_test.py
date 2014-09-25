#!/usr/bin/python

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
        print('PWM right: {} PWM middle: {} PWM left: {} PWM value: {}'.format(self.servo.BACKWARDS_VALUE,
                                                                               self.servo.STOP_VALUE,
                                                                               self.servo.FORWARD_VALUE, pwm_value))

    def test_speed_automatic(self):
        test_values = [100, 50, 0, -50, -100]

        for speed in test_values:
            self.test_speed(speed)
            time.sleep(2)

    def test_speed_interactive(self):
        speed = int(input('Speed: '))
        self.test_speed(speed)


print('Right - normal:')
tp_test = TowerProSG5010Test()
tp_test.test_speed_automatic()

print('Left - inverted:')
tp_test = TowerProSG5010Test(MotorPosition.LEFT)
print('Automatic mode:\n')
tp_test.test_speed_automatic()

print('Interactive mode:\n')
tp_test.test_speed_interactive()