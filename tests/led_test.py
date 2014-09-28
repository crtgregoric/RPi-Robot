#!/usr/bin/python

import sys
sys.path.append("/home/pi/shared")

from libraries.Adafruit_PWM_Servo_Driver import PWM
from pwm_objects.led import Led
import time


class LedTest():

    ADDRESS = 0x40
    FREQUENCY = 50
    CHANNEL = 6

    def __init__(self):
        self.pwm = PWM(self.ADDRESS)
        self.pwm.setPWMFreq(self.FREQUENCY)
        self.led = Led(self.pwm, self.CHANNEL)

    def test_brightness(self, brightness):
        pwm_value = self.led.set_brightness(brightness)
        print('PWM min: {} PWM max: {} PWM value: {} Brightness: {}'.format(self.led.OFF_VALUE, self.led.ON_VALUE,
                                                                            pwm_value, brightness))

    def test_brightness_automatic(self):
        test_values = [50, 100, 0, 25, 75]

        for brightness in test_values:
            self.test_brightness(brightness)
            time.sleep(2)

    def test_brightness_incremental(self):
        for brightness in range(101):
            self.led.set_brightness(brightness)

            if brightness % 10 == 0:
                print('Brightness: {}'.format(brightness))

            time.sleep(0.01)

    def test_brightness_interactive(self):
        while True:
            brightness = int(input('Brightness: '))
            self.test_brightness(brightness)


led_test = LedTest()

print('\nAutomatic mode:\n')
led_test.test_brightness_automatic()
led_test.test_brightness_incremental()

print('\nInteractive mode:\n')
led_test.test_brightness_interactive()