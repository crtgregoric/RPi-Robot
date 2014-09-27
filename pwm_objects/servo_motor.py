#!/usr/bin/python

from pwm_object import PWMObject


class ServoMotor(PWMObject):

    def __init__(self, pwm, channel, continuous, inverted=False):
        PWMObject.__init__(self, pwm, channel)
        self.continuous = continuous
        self.inverted = inverted

    def set_pwm_value(self, pwm_min_value, pwm_middle_value, pwm_max_value, input_value, abs_max_input_value):
        if abs(input_value) > abs_max_input_value:
            return

        if self.inverted:
            input_value = -input_value

        if input_value == 0 and self.continuous:
            self.pwm_off()
            return pwm_middle_value

        elif input_value > 0:
            delta = (pwm_max_value - pwm_middle_value)

        else:
            delta = (pwm_middle_value - pwm_min_value)

        pwm_value = int(pwm_middle_value + delta * (input_value / abs_max_input_value))
        self.pwm_on(pwm_value)

        return pwm_value