#!/usr/bin/python

# from libraries.Adafruit_PWM_Servo_Driver import PWM


class PWMObject():

    # ADDRESS = 0x40
    # FREQUENCY = 50

    def __init__(self, pwm, channel):
        # self.pwm = PWM(self.ADDRESS)
        # self.pwm.setPWMFreq(self.FREQUENCY)
        self.pwm = pwm
        self.channel = channel

    def pwm_on(self, time_on):
        self.pwm.setPWM(self.channel, 0, time_on)

    def pwm_on_advanced(self, time_off, time_on):
        self.pwm.setPWM(self.channel, time_off, time_on)

    def pwm_off(self):
        self.pwm.setPWM(self.channel, 0, 0)