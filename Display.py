import machine
import ssd1306

class OLED:
    i2c = machine.I2C(scl=machine.Pin(22), sda=machine.Pin(23))
    oled = ssd1306.SSD1306_I2C(128, 64, i2c)
    oled.text("Hello!", 0, 0)
    oled.show()

    def printStatus (self, temp, od, p1, p2, cool, char, val):
        self.oled.fill(0)
        self.oled.text(("Tmp:    " + temp), 0, 00)
        self.oled.text(("OD:     " + od), 0, 10)
        self.oled.text(("Pump 1: " + p1), 0, 20)
        self.oled.text(("Pump 2: " + p2), 0, 30)
        self.oled.text(("Cooler: " + cool), 0, 40)
        self.oled.text((char + ":      " + str(val)), 0, 50)
        try:
            self.oled.show()
        except:
            print ("failed to update screen")

    def printText (self, text):
        self.oled.fill(0)
        lines = text.split("\n")
        y = 0
        for l in lines:
            self.oled.text(l, 0, y)
            y = y + 10
        self.oled.show()
