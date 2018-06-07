import machine
import time
from od import *
from led import *
from Display import *
from pumps import *
from temperature import *
from cooling import *

led = Led(machine.PWM(machine.Pin(14), machine.Pin.OUT))
od = OD()
temp = TemperatureSensor()
display = OLED()
pump1 = Pump (machine.Pin(12), machine.Pin(13))
pump2 = Pump (machine.Pin(27), machine.Pin(33))
cooler = Cool()

while True:
    led.setPW(1023)
    time.sleep(1)
    led.setPW(0)
    time.sleep(1)
    display.printStatus(str(temp.readTemp()), str(od.rawRead()), pump1.status, pump2.status)

