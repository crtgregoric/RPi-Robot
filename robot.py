#!/usr/bin/python

from libraries.Adafruit_PWM_Servo_Driver import PWM
# from mock_objects.pwm_mock import PWM
import socket
import time
import os
import sys

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
    LED2_CHANNEL = 2
    LED3_CHANNEL = 3
    LED4_CHANNEL = 4
    LED5_CHANNEL = 5

    STATUS_LED_CHANNEL = 8

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
        self.led2 = Led(pwm, self.LED2_CHANNEL)
        self.led3 = Led(pwm, self.LED3_CHANNEL)
        self.led4 = Led(pwm, self.LED4_CHANNEL)
        self.led5 = Led(pwm, self.LED5_CHANNEL)

        self.led_array = [self.led3, self.led2, self.led4, self.led1, self.led5]

        self.status_led = Led(pwm, self.STATUS_LED_CHANNEL)
        self.status_led.set_brightness(100)

        self.socket, self.connection, self.client_address = None, None, None
        self.initialize_socket()

    def initialize_socket(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.HOST_NAME, self.PORT_NUMBER))

    def listen_for_connections(self):
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
        self.status_led.set_brightness(100)

    @staticmethod
    def start_video_stream():
        print('Starting video stream')
        os.system('sh start_stream.sh > /dev/null 2>&1 &')

    @staticmethod
    def stop_video_stream():
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
                self.listen_for_connections()

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
                self.left_motor.set_speed(px)
                self.right_motor.set_speed(py)
                print('Left: {}, Right: {}'.format(px, py))

            elif command_type == 1:
                angle = int((py / 100.0) * 90.0)
                self.camera_motor.set_angle(angle)

            elif command_type == 2:
                if py == 0:
                    self.set_led_brightness(0, len(self.led_array))

                else:
                    self.set_led_brightness(px, py)

        except TypeError:
            print('execute_command - Exception: TypeError')
            pass

        except ValueError:
            print('execute_command - Exception: ValueError')
            pass

    def set_led_brightness(self, brightness, led_state):
        if led_state == 0:
            number = 0

        elif led_state == 1:
            number = 1

        elif led_state == 2:
            number = 3

        else:
            number = len(self.led_array)

        for i in range(number):
            self.led_array[i].set_brightness(brightness)

        for i in range(number, len(self.led_array)):
            self.led_array[i].set_brightness(0)

    def shut_down(self):
        self.close_connection()
        self.status_led.set_brightness(0)
        self.pwm.setAllPWM(0, 0)


robot = Robot()

try:
    robot.listen_for_connections()
    robot.main_loop()

except KeyboardInterrupt as interrupt:
    print('\nmain_loop - Exception: KeyboardInterrupt\n')
    robot.shut_down()
    pass

except:
    print(sys.exc_info()[0])
    robot.shut_down()
    raise
