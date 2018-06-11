import machine

class Pump:

    def __init__(self, pforward, preverse):
        self.pforward = pforward
        self.pforward.freq(800)
        self.pforward.duty(0)
        self.preverse = preverse
        self.preverse.freq(800)
        self.preverse.duty(0)
        self.status = "stop"

    def activate (self, val, cool):
        if abs(val) > 1023:
            print("Invalid input. Choose a value between 1023 and -1023")
        else:
            if val < 0:
                self.pforward.duty(0)
                self.preverse.duty(-val)
                self.status = "reverse"
            elif val > 0:
                self.pforward.duty(val)
                self.preverse.duty(0)
                self.status = "forward"
            else:
                if cool.status == "on":
                    print("Cooler on. Can't stop pump")
                else:
                    self.pforward.duty(0)
                    self.preverse.duty(0)
                    self.status = "stop"

    def stop (self, cool):
        if cool.status == "on":
            print("Cooler on. ")
        else:
            self.preverse.duty(0)
            self.pforward.duty(0)
            self.status = "stop"