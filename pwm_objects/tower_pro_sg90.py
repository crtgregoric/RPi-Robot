#!/usr/bin/python

from servo_motor import ServoMotor


class TowerProSG90(ServoMotor):

    RIGHT_VALUE = 120
    MIDDLE_VALUE = 307
    LEFT_VALUE = 550

    ABS_MAX_ANGLE = 90.0

    CONTINUOUS = False

    def __init__(self, pwm, channel, inverted=False):
        ServoMotor.__init__(self, pwm, channel, self.CONTINUOUS, inverted)
        self.angle = 0

    def set_angle(self, angle):
        self.angle = angle
        pwm_value = self.set_pwm_value(self.RIGHT_VALUE, self.MIDDLE_VALUE, self.LEFT_VALUE, angle, self.ABS_MAX_ANGLE)
        return pwm_value