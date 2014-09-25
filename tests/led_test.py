#!/usr/bin/python

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
        print('PWM min: {} PWM max: {} PWM value: {}'.format(self.led.OFF_VALUE, self.led.ON_VALUE, pwm_value))

    def test_brightness_automatic(self):
        test_values = [50, 100, 0, 25, 75]

        for brightness in test_values:
            self.test_brightness(brightness)
            time.sleep(2)

    def test_brightness_interactive(self):
        brightness = int(input('Brightness: '))
        self.test_brightness(brightness)


led_test = LedTest()

print('\nAutomatic mode:\n')
led_test.test_brightness_automatic()

print('\nInteractive mode:\n')
led_test.test_brightness_interactive()