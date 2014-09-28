#!/usr/bin/python

from libraries.Adafruit_PWM_Servo_Driver import PWM

from pwm_objects.tower_pro_sg5010 import TowerProSG5010
from pwm_objects.tower_pro_sg90 import TowerProSG90
from pwm_objects.led import Led

from helpers.motor_position import MotorPosition
from helpers.servo_data import TowerProSG5010RightData, TowerProSG5010LeftData, TowerProSG90Data


class Robot():

    ADDRESS = 0x40
    FREQUENCY = 50

    LEFT_MOTOR_CHANNEL = 0
    RIGHT_MOTOR_CHANNEL = 15
    CAMERA_MOTOR_CHANNEL = 7

    LED1_CHANNEL = 6

    def __init__(self):
        pwm = PWM(self.ADDRESS)
        pwm.setPWMFreq(self.FREQUENCY)

        self.right_motor = TowerProSG5010(pwm, self.RIGHT_MOTOR_CHANNEL, TowerProSG5010RightData, MotorPosition.RIGHT)
        self.left_motor = TowerProSG5010(pwm, self.LEFT_MOTOR_CHANNEL, TowerProSG5010LeftData, MotorPosition.LEFT)

        self.camera_motor = TowerProSG90(pwm, self.CAMERA_MOTOR_CHANNEL, TowerProSG90Data, True)

        self.led1 = Led(pwm, self.LED1_CHANNEL)


robot = Robot()