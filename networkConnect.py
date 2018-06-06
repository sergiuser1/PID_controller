import time
import network

sta_if = network.WLAN(network.STA_IF)
tryAgain = True

while tryAgain:
    print('connecting to network...')
    sta_if.active(True)
    sta_if.connect('Internet_of_Mussels', 'Feather_HUZZAH32')
    if not sta_if.isconnected():
        inp = input ("Failed to connect to network. Try again? [y / n] ")
        if inp == "n": TryAgain = False
    else:
        TryAgain = False
        print('network config:', sta_if.ifconfig())