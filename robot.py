#!/usr/bin/python

from libraries.Adafruit_PWM_Servo_Driver import PWM
# from mock_objects.pwm_mock import PWM
import socket
import math
import os
import time

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
    HOST_NAME = 'rpi.local'
    # HOST_NAME = 'cromartie.local'
    PORT_NUMBER = 6000
    BUFFER_SIZE = 1024

    def __init__(self):
        pwm = PWM(self.I2C_ADDRESS)
        pwm.setPWMFreq(self.FREQUENCY)
        self.pwm = pwm

        self.right_motor = TowerProSG5010(pwm, self.RIGHT_MOTOR_CHANNEL, TowerProSG5010RightData, MotorPosition.RIGHT)
        self.left_motor = TowerProSG5010(pwm, self.LEFT_MOTOR_CHANNEL, TowerProSG5010LeftData, MotorPosition.LEFT)

        self.camera_motor = TowerProSG90(pwm, self.CAMERA_MOTOR_CHANNEL, TowerProSG90Data, True)

        self.led1 = Led(pwm, self.LED1_CHANNEL)

        self.socket, self.connection, self.client_address = None, None, None
        self.initialize_socket()

    def initialize_socket(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.HOST_NAME, self.PORT_NUMBER))
        self.socket.listen(1)
        print('Listening for connections.')

        (self.connection, self.client_address) = self.socket.accept()
        print('Connected by: {}'.format(self.client_address[0]))

        self.start_video_stream()

    def reply(self, data):
        self.connection.send(data)

    def close_connection(self):
        self.stop_video_stream()

        if self.connection:
            self.connection.close()

        if self.socket:
            self.socket.close()

        if self.client_address:
            print('Connection to client {} closed.\n'.format(self.client_address[0]))

        self.socket, self.connection, self.client_address = None, None, None
        self.pwm.setAllPWM(0, 0)

    def start_video_stream(self):
        print('Starting video stream')
        os.system('sh start_stream.sh > /dev/null 2>&1 &')

    def stop_video_stream(self):
        print('Stopping video stream')
        os.system('pkill gst-launch-1.0')
        os.system('pkill raspivid')

    def main_loop(self):
        while True:
            data = self.connection.recv(self.BUFFER_SIZE)

            if data:
                self.parse_data(data)
            else:
                self.close_connection()
                time.sleep(2)
                self.initialize_socket()

    def parse_data(self, data):
        commands = data.split('|')

        try:
            for command in commands:
                if command:
                    split_command = command.split(' ')
                    command_type, px, py = split_command[0], split_command[1], split_command[2]
                    self.execute_command(command_type, px, py)

        except IndexError:
            print('parse_data - Exception: IndexError')
            pass

    def execute_command(self, command_type, px, py):
        try:
            command_type, px, py = int(command_type), int(px), int(py)

            if command_type == 0:
                self.set_motors_speed(px, py)

            elif command_type == 1:
                angle = int((py / 100.0) * 90.0)
                self.camera_motor.set_angle(angle)

            elif command_type == 2:
                self.led1.set_brightness(px)

        except TypeError:
            print('execute_command - Exception: TypeError')
            pass

        except ValueError:
            print('execute_command - Exception: ValueError')
            pass

    def set_motors_speed(self, px, py):
        distance = math.sqrt(px**2 + py**2)

        if px > 0:
            right_speed = py
            left_speed = distance if py > 0 else -distance
        else:
            right_speed = distance if py > 0 else -distance
            left_speed = py

        self.right_motor.set_speed(int(right_speed))
        self.left_motor.set_speed(int(left_speed))

        print('Right: {}, Left: {}'.format(int(right_speed), int(left_speed)))

robot = None

try:
    robot = Robot()
    robot.main_loop()

except KeyboardInterrupt as interrupt:
    print('\nmain_loop - Exception: KeyboardInterrupt\n')
    if robot:
        robot.close_connection()
    pass