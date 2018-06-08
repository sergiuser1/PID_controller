# import inbuilt time and machine modules
import time
import machine

#import self-written modules
from od import *
from led import *
from Display import *
from pumps import *
from temperature import *
from cooling import *
from networkConnect import *

# Import mqtt library
from simple import MQTTClient

# Instantiate objects for all classes
display = OLED()
display.printText("Initializing...")

led = Led(machine.PWM(machine.Pin(14), machine.Pin.OUT))
od = OD()
temp = TemperatureSensor()
pump1 = Pump (machine.Pin(12, machine.Pin.OUT), machine.Pin(13, machine.Pin.OUT))
pump2 = Pump (machine.Pin(27, machine.Pin.OUT), machine.Pin(33, machine.Pin.OUT))
cooler = Cool()

# Connect to WiFi
tryConnect(display)

# Set to your Adafruit IO key & username below.
pwd = '5c0f28d19a0a4e5b9890ea6e3538b1d7'
user1 = 'bossebandowski' # See https://accounts.adafruit.com

# Define how long the system is meant to run [s]
runtime = 3600

# Define data frequency (how many seconds between each data point?)
rest = 60

def run(t, rest):
    display.printText("Start!")
    time.sleep(1)
    pump2.activate(1)
    cooler.superCool(pump2)

    i = 0

    while True:
        if (i % rest) == 0:
            castData()
        display.printStatus(str(temp.readTemp()), str(od.rawRead()), pump1.status, pump2.status, cooler.status)
        time.sleep(1)
        i = i + 1

        if temp.readTemp() < 19:
            cooler.basicCool()
            pump1.stop()
            pump2.stop()
            display.printText("Done")
            break

def castTemp(server="io.adafruit.com", user = user1, password = pwd):
    c = MQTTClient("umqtt_client", server, user = user, password = password, keepalive = 3600)
    c.connect()
    c.publish(b"{}/f/temperature".format(user), b"{}".format(temp.readTemp()))
    c.disconnect()

def castOD(server="io.adafruit.com", user = user1, password = pwd):
    c = MQTTClient("umqtt_client", server, user = user, password = password, keepalive = 3600)
    c.connect()
    c.publish(b"{}/f/od".format(user), b"{}".format(od.rawRead()))
    c.disconnect()

def castPump1(server="io.adafruit.com", user = user1, password = pwd):
    c = MQTTClient("umqtt_client", server, user = user, password = password, keepalive = 3600)
    c.connect()
    if pump1.status == "forward":
        c.publish(b"{}/f/pump-1-activity".format(user), b"{}".format(1))
    elif pump1.status == "reverse":
        c.publish(b"{}/f/pump-1-activity".format(user), b"{}".format(-1))
    else:
        c.publish(b"{}/f/pump-1-activity".format(user), b"{}".format(0))
    c.disconnect()

def castPump2(server="io.adafruit.com", user = user1, password = pwd):
    c = MQTTClient("umqtt_client", server, user = user, password = password, keepalive = 3600)
    c.connect()
    if pump2.status == "forward":
        c.publish(b"{}/f/pump-2-activity".format(user), b"{}".format(1))
    elif pump2.status == "reverse":
        c.publish(b"{}/f/pump-2-activity".format(user), b"{}".format(-1))
    else:
        c.publish(b"{}/f/pump-2-activity".format(user), b"{}".format(0))
    c.disconnect()

def castCooler(server="io.adafruit.com", user = user1, password = pwd):
    c = MQTTClient("umqtt_client", server, user = user, password = password, keepalive = 3600)
    c.connect()
    if cooler.status == "on":
        c.publish(b"{}/f/cooler-activity".format(user), b"{}".format(12))
    else:
        c.publish(b"{}/f/cooler-activity".format(user), b"{}".format(5))
    c.disconnect()

def castData():
    display.printText("Casting data...")
    castCooler()
    castOD()
    castPump1()
    castPump2()
    castTemp()

run(runtime, rest)