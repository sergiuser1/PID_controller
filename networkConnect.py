import time
import network

def tryConnect():
    sta_if = network.WLAN(network.STA_IF)

    print('connecting to network...')
    sta_if.active(True)
    sta_if.connect('Internet_of_Mussels', 'Feather_HUZZAH32')
    if not sta_if.isconnected():
        print ("Failed to connect to network. ")
    else:
        print('network config:', sta_if.ifconfig())