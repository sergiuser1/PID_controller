# import inbuilt time and machine modules
import time
import machine
from math import floor

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
pump1 = Pump (machine.PWM(machine.Pin(12, machine.Pin.OUT)), machine.PWM(machine.Pin(13, machine.Pin.OUT)), False)
pump2 = Pump (machine.PWM(machine.Pin(27, machine.Pin.OUT)), machine.PWM(machine.Pin(33, machine.Pin.OUT)), True)
cooler = Cool()

# temperature PID init
temppid = [20, 6, 30]
temperr = [0]
optTemp = 19

# OD PID init
odpid = [0, 0, 0]
oderr = [0]
optOD = 590

# Water level control
wlOut = machine.Pin(21, machine.Pin.OUT)
wlOut.value(1)
wl = machine.ADC(machine.Pin(36))
wl.atten(3)
wl.width(machine.ADC.WIDTH_10BIT)

# initial algae parameters

cia = 50000.0
cim = 20000.0
cd = 20000.0
pr = 1.25
vm = 2000.0

# Connect to WiFi
tryConnect(display)

# Set to your Adafruit IO key & username below.
pwd = '5c0f28d19a0a4e5b9890ea6e3538b1d7'
user1 = 'bossebandowski' # See https://accounts.adafruit.com

# Define data frequency (how many seconds between each data point?)
rest = 15

def run(rest, c, cia, cim, cd, pr, vm):
    display.printText("Start!")
    time.sleep(1)
    odVal = 0

    i = 0
    p1t = 0
    marker = 0

    while True:

        # Cast data

        if (i % rest) == 0:
            try:
                castData(c)
            except:
                print ("failed castData()")
                c = connect2Client()
                subscribePID(c)

        # Check for PID updates

        try:
            c.check_msg()
        except:
            print ("failed check_msg")
            c = connect2Client()

        # Update screen

        if (i % 3) == 0:
            display.printStatus(str(temp.readTemp()), str(odVal), str(pump1.getVal()), str(pump2.getVal()), cooler.status, "p", odpid[0])
        if (i % 3) == 1:
            display.printStatus(str(temp.readTemp()), str(odVal), str(pump1.getVal()), str(pump2.getVal()), cooler.status, "i", odpid[1])
        if (i % 3) == 2:
            display.printStatus(str(temp.readTemp()), str(odVal), str(pump1.getVal()), str(pump2.getVal()), cooler.status, "d", odpid[2])


        # Temp Control

        temppw = toPW(getValPID (temppid, temperr, optTemp, temp.readTemp()))

        if (temppw > 500):
            cooler.superCool(pump2)
        else:
            cooler.basicCool()

        if temppw <1023:
            pump2.activate(-temppw, cooler)
        else:
            pump2.activate(1023, cooler)

        # OD Control - use this OR the model below!

        # turn pump off to take od reading

        if i % 10 == 0:
            currentval = pump2.getVal()
            if cooler.status == "on":
                cooler.basicCool()
                pump2.stop(cooler)
                time.sleep(2)
                odVal = od.rawRead()
                pump2.activate(currentval, cooler)
            else:
                pump2.stop(cooler)
                time.sleep(2)
                odVal = od.rawRead()
                pump2.activate(currentval, cooler)

            odpw = toPW(getValPID(odpid, oderr, optOD, odVal))
            pump1.activate(odpw, cooler)

        # Algae Control

        """# Update concentrations depending on growth and filtration
        cia = cia * 2.0**(1/84600)
        cim = cim - 2.0

        # Update pump 1 remaining time if the pump is running (p1t)
        if p1t >= 0:
            p1t = p1t - 1.0
        else:
            marker = 0

        # Check if concentration is too low. If yes, calculate pump runtime based on algae parameters. Set algae
        # concentration in mussel tank to desired value
        if cim < 19500:
            p1t = - (vm * (cim - cd))/(pr*(cia - cd))
            marker = 1
            cim = cd

        # start pump if need be, else stop pump. Update volume
        if marker == 1:
            pump1.activate(1023, cooler)
            vm = vm + 1.25
        else:
            pump1.stop(cooler)"""

        # Increment i
        i = i + 1

        # Pause
        time.sleep(1)

def checkWL ():
    if wl.read() > 1000:
        return False
    else:
        for i in range (5):
            if wl.read() > 1000: return False
        return True

def changeWL():
    if checkWL():
        pass

def toPW (val):
    if val > 50:
        return 1023
    elif val <= 50 and val > 30:
        return 750
    elif val <= 30 and val > 10:
        return 500
    else:
        return 0

def getValPID (pid, errHistory, tOpt, tAct):
    val = pid[0] * (tAct - tOpt) + pid[1] * sum (errHistory) + pid[2] * ((tAct - tOpt) - errHistory[-1])
    errHistory.append(tAct - tOpt)
    if len(errHistory) > 20:
        del errHistory[0]
    return val

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
    client.publish(b"{}/f/pump-1-activity".format(user), b"{}".format(pump1.getVal()))

def castPump2(client, user = user1):
    client.publish(b"{}/f/pump-2-activity".format(user), b"{}".format(pump2.getVal()))

def castCooler(client, user = user1):
    if cooler.status == "on":
        client.publish(b"{}/f/cooler-activity".format(user), b"{}".format(12))
    else:
        client.publish(b"{}/f/cooler-activity".format(user), b"{}".format(5))

def callback(topic, message):
    char = topic [-1]
    msg = str(message)
    val = int(str(msg)[2:(len(msg)-1)])
    if char == 112:
        odpid[0] = val
    elif char == 105:
        odpid[1] = val
    elif char == 100:
        odpid[2] = val

def subscribePID(client, user = user1):
    client.set_callback(callback)
    client.subscribe(b"{}/f/pid-p".format(user))
    client.subscribe(b"{}/f/pid-i".format(user))
    client.subscribe(b"{}/f/pid-d".format(user))
    # once subscribed, all data sent to the feed is stored in a queue. To access the queue, use client.check_msg().
    # Change the callback method to assign the input to the correct P, I, D when calibrating

def castData(c):
    castCooler(c)
    castOD(c)
    castPump1(c)
    castPump2(c)
    castTemp(c)

# Connect to client and initialize client object
client = connect2Client()
subscribePID(client)

run(rest, client, cia, cim, cd, pr, vm)