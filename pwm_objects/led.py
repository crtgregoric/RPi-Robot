#!/usr/bin/python

from pwm_object import PWMObject


class Led(PWMObject):

    OFF_VALUE = 0
    ON_VALUE = 4095

    MAX_BRIGHTNESS = 100.0

    def __init__(self, pwm, channel):
        PWMObject.__init__(self, pwm, channel)
        self.brightness = 0

    def set_brightness(self, brightness):
        if brightness > self.MAX_BRIGHTNESS:
            return

        pwm_value = int((self.ON_VALUE - self.OFF_VALUE) * (brightness / self.MAX_BRIGHTNESS))
        self.pwm_on(pwm_value)
        self.brightness = brightness

        return pwm_value