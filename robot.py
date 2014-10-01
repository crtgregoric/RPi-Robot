#!/usr/bin/python

from libraries.Adafruit_PWM_Servo_Driver import PWM
import socket

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

    HOST_NAME = 'rpi.local'
    PORT_NUMBER = 1234

    def __init__(self):
        pwm = PWM(self.ADDRESS)
        pwm.setPWMFreq(self.FREQUENCY)

        self.right_motor = TowerProSG5010(pwm, self.RIGHT_MOTOR_CHANNEL, TowerProSG5010RightData, MotorPosition.RIGHT)
        self.left_motor = TowerProSG5010(pwm, self.LEFT_MOTOR_CHANNEL, TowerProSG5010LeftData, MotorPosition.LEFT)

        self.camera_motor = TowerProSG90(pwm, self.CAMERA_MOTOR_CHANNEL, TowerProSG90Data, True)

        self.led1 = Led(pwm, self.LED1_CHANNEL)

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.HOST_NAME, self.PORT_NUMBER))
        self.socket.listen(1)

        print('Ready.')

        (self.connection, self.client_address) = self.socket.accept()
        print('Connected by: {}', self.client_address[0])

    def main_loop(self):
        while True:
            data = self.connection.recv(1024)

            if data:
                command = str(data).split()
                value = int(command[1])

                if command[0] == '0':
                    self.right_motor.set_speed(value)

                elif command[0] == '1':
                    self.left_motor.set_speed(value)

                elif command[0] == '2':
                    self.camera_motor.set_angle(value)

                elif command[0] == '3':
                    self.led1.set_brightness(value)

                elif command[0] == '4':
                    self.connection.close()
                    self.socket.close()
                    break

            else:
                self.connection.close()
                self.socket.close()
                break


robot = Robot()
robot.main_loop()