import machine

class Led :

    def __init__(self, pin):
        self.ledpin = pin
        self.ledpin.freq(50000)
        self.ledpin.duty(1023)

    def setPW (self, val):

        if (val > 1023 or val < 0):
            print("Invalid input")
        else:
            self.ledpin.duty(val)
            print("PW set to " + str((val / 1023) * 100) + "%")