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
pump1 = Pump (machine.PWM(machine.Pin(12, machine.Pin.OUT)), machine.PWM(machine.Pin(13, machine.Pin.OUT)))
pump2 = Pump (machine.PWM(machine.Pin(27, machine.Pin.OUT)), machine.PWM(machine.Pin(33, machine.Pin.OUT)))
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
    pump2.activate(1023, cooler)
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
            pump1.stop(cooler)
            pump2.stop(cooler)
            client.disconnect()
            display.printText("Done")
            break

def connect2Client (server="io.adafruit.com", user = user1, password = pwd):
    c = MQTTClient("umqtt_client", server, user=user, password=password, keepalive=3600)
    c.connect()
    return c

def disconnectClient (client):
    client.disconnect()

def castTemp(client, user = user1):
    client.publish(b"{}/f/temperature".format(user), b"{}".format(temp.readTemp()))

def castOD(client, user = user1):
    client.publish(b"{}/f/od".format(user), b"{}".format(od.rawRead()))

def castPump1(client, user = user1):
    if pump1.status == "forward":
        client.publish(b"{}/f/pump-1-activity".format(user), b"{}".format(1))
    elif pump1.status == "reverse":
        client.publish(b"{}/f/pump-1-activity".format(user), b"{}".format(-1))
    else:
        client.publish(b"{}/f/pump-1-activity".format(user), b"{}".format(0))

def castPump2(client, user = user1):
    if pump2.status == "forward":
        client.publish(b"{}/f/pump-2-activity".format(user), b"{}".format(1))
    elif pump2.status == "reverse":
        client.publish(b"{}/f/pump-2-activity".format(user), b"{}".format(-1))
    else:
        client.publish(b"{}/f/pump-2-activity".format(user), b"{}".format(0))

def castCooler(client, user = user1):
    if cooler.status == "on":
        client.publish(b"{}/f/cooler-activity".format(user), b"{}".format(12))
    else:
        client.publish(b"{}/f/cooler-activity".format(user), b"{}".format(5))

def callback(topic, message):
    print (topic, ":", message)

def subscribePID(client, user = user1):
    client.set_callback(callback)
    client.subscribe(b"{}/f/pid-p".format(user))
    client.subscribe(b"{}/f/pid-i".format(user))
    client.subscribe(b"{}/f/pid-d".format(user))
    # once subscribed, all data sent to the feed is stored in a queue. To access the queue, use client.check_msg().
    # Change the callback method to assign the input to the correct P, I, D when calibrating

def castData():
    display.printText("Casting data...")
    castCooler(client)
    castOD(client)
    castPump1(client)
    castPump2(client)
    castTemp(client)

# Connect to client and initialize client object
client = connect2Client()

run(runtime, rest)