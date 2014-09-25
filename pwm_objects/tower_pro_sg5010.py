#!/usr/bin/python

from servo_motor import ServoMotor
from helpers.motor_position import MotorPosition


class TowerProSG5010(ServoMotor):

    BACKWARDS_VALUE = 0
    STOP_VALUE = 0
    FORWARD_VALUE = 0

    ABS_MAX_SPEED = 100.0

    MOTOR_POSITION = MotorPosition.RIGHT

    def __init__(self, pwm, channel, position):
        inverted = True if position == MotorPosition.LEFT else False
        ServoMotor.__init__(self, pwm, channel, inverted)
        self.MOTOR_POSITION = position
        self.speed = 0

    def set_speed(self, speed):
        self.set_pwm_value(self.BACKWARDS_VALUE, self.STOP_VALUE, self.FORWARD_VALUE, speed, self.ABS_MAX_SPEED)
        self.speed = speed