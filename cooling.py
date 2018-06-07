import machine

class Cool :
    coolPin = machine.Pin(15, machine.Pin.OUT)

    def __init__(self):
        self.coolPin.value(1)
        self.status = "off"

    def superCool (self, pump):
        if pump.status == "stop":
            self.coolPin.value(1)
            self.status = "off"
        else:
            self.coolPin.value(0)
            self.status = "on"

    def basicCool (self):
        self.coolPin.value(1)
        self.status = "off"
