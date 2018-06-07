import time
import machine
from od import *
from led import *
from Display import *
from pumps import *
from temperature import *
from cooling import *
# Import standard python modules.
from simple import MQTTClient

led = Led(machine.PWM(machine.Pin(14), machine.Pin.OUT))
od = OD()
temp = TemperatureSensor()
display = OLED()
pump1 = Pump (machine.Pin(12), machine.Pin(13))
pump2 = Pump (machine.Pin(27), machine.Pin(33))
cooler = Cool()

#while True:
#    led.setPW(1023)
#    time.sleep(1)
#    led.setPW(0)
#    time.sleep(1)
#    display.printStatus(str(temp.readTemp()), str(od.rawRead()), pump1.status, pump2.status)


# Import Adafruit IO MQTT client.


# Set to your Adafruit IO key & username below.
pwd      = '9d2178d712964240a8e1cb5892ffd5c6'
user1 = 'sergiuser' # See https://accounts.adafruit.com
                                                    # to find your username.


#from umqtt.simple import MQTTClient

# Test reception e.g. with:
# mosquitto_sub -t foo_topic

def main(server="io.adafruit.com", user = user1, password = pwd):
    c = MQTTClient("umqtt_client", server, user = user, password = password, keepalive = 3600)
    c.connect()
    print('asdasd')
    for i in range(10):
        c.publish(b"{}/f/foo_topic".format(user), b"{}".format(i**2))
        time.sleep(1)
    c.disconnect()

if __name__ == "__main__":
    main()