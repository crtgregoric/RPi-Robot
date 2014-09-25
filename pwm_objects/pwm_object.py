#!/usr/bin/python


class PWMObject():

    def __init__(self, pwm, channel):
        self.pwm = pwm
        self.channel = channel

    def pwm_on(self, time_on):
        self.pwm.setPWM(self.channel, 0, time_on)

    def pwm_on_advanced(self, time_off, time_on):
        self.pwm.setPWM(self.channel, time_off, time_on)

    def pwm_off(self):
        self.pwm.setPWM(self.channel, 0, 0)