#!/usr/bin/python

from pwm_objects.pwm_object import PWMObject


class TowerProSG5010(PWMObject):

    def __init__(self, channel):
        PWMObject.__init__(channel)