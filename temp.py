import machine
import time
import ssd1306
from Display import *
from pumps import *

def initialize ():

    # Initialize temp
    temppin = machine.ADC(machine.Pin(39))
    temppin.atten(3)

    # Initialize od
    odpin = machine.ADC(machine.Pin(34))
    odpin.atten(3)

    # Initialize LED
    ledpin = machine.PWM(machine.Pin(14, machine.Pin.OUT))
    ledpin.freq(800)
    ledpin.duty(1023)

    # Initialize pumps

    pump1 = Pump(machine.PWM(machine.Pin(13, machine.Pin.OUT)), machine.PWM(machine.Pin(12, machine.Pin.OUT)))
    pump2 = Pump(machine.PWM(machine.Pin(27, machine.Pin.OUT)), machine.PWM(machine.Pin(33, machine.Pin.OUT)))
    pump1forward = machine.PWM(machine.Pin(13, machine.Pin.OUT))
    pump1reverse = machine.PWM(machine.Pin(12, machine.Pin.OUT))
    pump2forward = machine.PWM(machine.Pin(27, machine.Pin.OUT))
    pump2reverse = machine.PWM(machine.Pin(33, machine.Pin.OUT))

    # Initialize display
    i2c = machine.I2C(scl=machine.Pin(22), sda=machine.Pin(23))
    oled=ssd1306.SSD1306_I2C(128, 64, i2c)
    oled.text("Hello!", 0, 0)
    oled.show()

    for i in range (5):
        ledpin.duty(0)
        time.sleep(0.2)
        ledpin.duty(1023)
        time.sleep(0.2)
        oled.fill(0)
        oled.text(str(i+1) +"...", 0, 0)
        oled.show()

    printStatus(oled)


