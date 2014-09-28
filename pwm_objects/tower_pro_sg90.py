#!/usr/bin/python

from servo_motor import ServoMotor


class TowerProSG90(ServoMotor):

    def __init__(self, pwm, channel, servo_data, inverted=False):
        ServoMotor.__init__(self, pwm, channel, servo_data.CONTINUOUS, inverted)

        self.right_value = servo_data.LOW_VALUE
        self.middle_value = servo_data.MID_VALUE
        self.left_value = servo_data.HIGH_VALUE

        self.abs_max_angle = servo_data.ABS_MAX_UNIT

        self.angle = 0

    def set_angle(self, angle):
        self.angle = angle
        pwm_value = self.set_pwm_value(self.left_value, self.middle_value, self.right_value, angle, self.abs_max_angle)
        return pwm_value