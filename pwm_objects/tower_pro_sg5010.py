#!/usr/bin/python

from servo_motor import ServoMotor
from helpers.servo_data import *
from helpers.motor_position import MotorPosition


class TowerProSG5010(ServoMotor):

    def __init__(self, pwm, channel, position):
        inverted = True if position == MotorPosition.RIGHT else False
        ServoMotor.__init__(self, pwm, channel, TowerProSG5010Data.CONTINUOUS, inverted)
        self.motor_position = position

        if self.motor_position == MotorPosition.LEFT:
            self.backwards_value = TowerProSG5010LeftData.LOW_VALUE
            self.stop_value = TowerProSG5010LeftData.MID_VALUE
            self.forward_value = TowerProSG5010LeftData.HIGH_VALUE

        elif self.motor_position == MotorPosition.RIGHT:
            self.backwards_value = TowerProSG5010RightData.LOW_VALUE
            self.stop_value = TowerProSG5010RightData.MID_VALUE
            self.forward_value = TowerProSG5010RightData.HIGH_VALUE

        self.abs_max_speed = TowerProSG5010Data.ABS_MAX_UNIT
        self.speed = 0

    def set_speed(self, speed):
        self.speed = speed
        pwm_value = self.set_pwm_value(self.backwards_value, self.stop_value,
                                       self.forward_value, speed, self.abs_max_speed)
        return pwm_value