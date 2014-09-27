#!/usr/bin/python

from servo_motor import ServoMotor
from helpers.servo_data import TowerProSG90Data


class TowerProSG90(ServoMotor):

    def __init__(self, pwm, channel, inverted=False):
        ServoMotor.__init__(self, pwm, channel, TowerProSG90Data.CONTINUOUS, inverted)

        self.inverted = inverted

        self.right_value = TowerProSG90Data.LOW_VALUE
        self.middle_value = TowerProSG90Data.MID_VALUE
        self.left_value = TowerProSG90Data.HIGH_VALUE

        self.abs_max_angle = TowerProSG90Data.ABS_MAX_UNIT

        self.angle = 0

    def set_angle(self, angle):
        self.angle = angle
        pwm_value = self.set_pwm_value(self.right_value, self.middle_value, self.left_value, angle, self.abs_max_angle)
        return pwm_value