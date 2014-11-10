#!/usr/bin/python

# from libraries.Adafruit_PWM_Servo_Driver import PWM
from mock_objects.pwm_mock import PWM
import socket

from pwm_objects.tower_pro_sg5010 import TowerProSG5010
from pwm_objects.tower_pro_sg90 import TowerProSG90
from pwm_objects.led import Led

from helpers.motor_position import MotorPosition
from helpers.servo_data import TowerProSG5010RightData, TowerProSG5010LeftData, TowerProSG90Data


class Robot():

    # PWM servo driver settings
    I2C_ADDRESS = 0x40
    FREQUENCY = 50

    # PWM channels
    LEFT_MOTOR_CHANNEL = 0
    RIGHT_MOTOR_CHANNEL = 15
    CAMERA_MOTOR_CHANNEL = 7

    LED1_CHANNEL = 1

    # Connection settings
    # HOST_NAME = 'rpi.local'
    HOST_NAME = 'cromartie.local'
    PORT_NUMBER = 1234
    BUFFER_SIZE = 1024

    def __init__(self):
        pwm = PWM(self.I2C_ADDRESS)
        pwm.setPWMFreq(self.FREQUENCY)

        self.right_motor = TowerProSG5010(pwm, self.RIGHT_MOTOR_CHANNEL, TowerProSG5010RightData, MotorPosition.RIGHT)
        self.left_motor = TowerProSG5010(pwm, self.LEFT_MOTOR_CHANNEL, TowerProSG5010LeftData, MotorPosition.LEFT)

        self.camera_motor = TowerProSG90(pwm, self.CAMERA_MOTOR_CHANNEL, TowerProSG90Data, True)

        self.led1 = Led(pwm, self.LED1_CHANNEL)

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.HOST_NAME, self.PORT_NUMBER))
        self.socket.listen(1)
        print('Ready.')

        (self.connection, self.client_address) = self.socket.accept()
        print('Connected by: {}'.format(self.client_address[0]))

    def main_loop(self):
        while True:
            data = self.connection.recv(self.BUFFER_SIZE)

            if data:
                self.parse_data(data)
            else:
                break

    def parse_data(self, data):
        commands = data.split("|")

        try:
            for command in commands:
                if command:
                    split_command = command.split(" ")
                    command_type, px, py = split_command[0], split_command[1], split_command[2]
                    self.execute_command(command_type, px, py)

        except IndexError:
            print("parse_data - Exception: IndexError")
            pass

    def execute_command(self, command_type, px, py):
        try:
            command_type, px, py = int(command_type), int(px), int(py)

            if command_type == 0:
                print("Drive")

            elif command_type == 1:
                angle = int((py / 100.0) * 90.0)
                print(angle)
                self.camera_motor.set_angle(angle)

            elif command_type == 2:
                self.led1.set_brightness(py)

        except TypeError:
            print("execute_command - Exception: TypeError")
            pass

        except ValueError:
            print("execute_command - Exception: ValueError")
            pass

    def reply(self, data):
        self.connection.send(data)

    def close_connection(self):
        self.connection.close()
        self.socket.close()
        print('Connection closed.')


robot = Robot()
try:
    robot.main_loop()
except KeyboardInterrupt as interrupt:
    print("main_loop - Exception: KeyboardInterrupt")
    pass
robot.close_connection()
