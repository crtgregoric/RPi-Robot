#!/usr/bin/python

from libraries.Adafruit_PWM_Servo_Driver import PWM


class PWMObject():

    ADDRESS = 0x40
    FREQUENCY = 50

    def __init__(self, channel):
        self.pwm = PWM(self.ADDRESS)
        self.pwm.setPWMFreq(self.FREQUENCY)

        self.channel = channel

    def stop(self):
        self.pwm.setPWM(self.channel, 0, 0)