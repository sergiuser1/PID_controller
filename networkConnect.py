import time
import network
from Display import *

def tryConnect(display):
    sta_if = network.WLAN(network.STA_IF)

    display.printText("connecting to \nnetwork...")
    sta_if.active(True)
    sta_if.connect('Internet_of_Mussels', 'Feather_HUZZAH32')
    time.sleep(5)
    if not sta_if.isconnected():
        display.printText("Failed to connect")
    else:
        display.printText("Connection \nsuccessful")
        time.sleep(2)