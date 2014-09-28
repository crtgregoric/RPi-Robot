#!/usr/bin/python

from servo_motor import ServoMotor
from helpers.motor_position import MotorPosition


class TowerProSG5010(ServoMotor):

    def __init__(self, pwm, channel, servo_data, position):
        inverted = True if position == MotorPosition.RIGHT else False
        ServoMotor.__init__(self, pwm, channel, servo_data.CONTINUOUS, inverted)
        self.motor_position = position

        self.backwards_value = servo_data.LOW_VALUE
        self.stop_value = servo_data.MID_VALUE
        self.forward_value = servo_data.HIGH_VALUE

        self.abs_max_speed = servo_data.ABS_MAX_UNIT
        self.speed = 0

    def set_speed(self, speed):
        self.speed = speed
        pwm_value = self.set_pwm_value(self.backwards_value, self.stop_value,
                                       self.forward_value, speed, self.abs_max_speed)
        return pwm_value