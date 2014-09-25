#!/usr/bin/python

from pwm_object import PWMObject


class ServoMotor(PWMObject):

    def __init__(self, pwm, channel, inverted=False):
        PWMObject.__init__(self, pwm, channel)
        self.inverted = inverted

    def set_pwm_value(self, pwm_min_value, pwm_middle_value, pwm_max_value, input_value, abs_max_input_value):
        if abs(input_value) > abs_max_input_value:
            return

        pwm_delta = 0

        if input_value > 0:
            pwm_delta = (pwm_max_value - pwm_middle_value) * (input_value / abs_max_input_value)

        elif input_value < 0:
            pwm_delta = (pwm_middle_value - pwm_min_value) * (input_value / abs_max_input_value)

        else:
            self.pwm_off()

        pwm_value = int(pwm_middle_value + (pwm_delta if not self.inverted else -pwm_delta))
        self.pwm_on(pwm_value)

        return pwm_value