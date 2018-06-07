import machine

class Pump:

    def __init__(self, pforward, preverse):
        self.pforward = pforward
        self.pforward.value(0)
        self.preverse = preverse
        self.preverse.value(0)
        self.status = "stop"

    def activate (self, val):
        if val == 1:
            self.pforward.value(1)
            self.preverse.value(0)
            self.status = "forward"
        elif val == 0:
            self.pforward.value(0)
            self.preverse.value(0)
            self.status = "stop"
        elif val == -1:
            self.pforward.value(0)
            self.preverse.value(1)
            self.status = "reverse"
        else:
            print ("Invalid input. Choose 1 or -1")

    def stop (self):
        self.preverse.value(0)
        self.pforward.value(0)
        self.status = "stop"