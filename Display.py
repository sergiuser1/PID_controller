import machine
import ssd1306

class OLED:
    i2c = machine.I2C(scl=machine.Pin(22), sda=machine.Pin(23))
    oled = ssd1306.SSD1306_I2C(128, 64, i2c)
    oled.text("Hello!", 0, 0)
    oled.show()

    def printStatus (self, temp, od, p1, p2):
        self.oled.fill(0)
        self.oled.text(("Tmp:    " + temp), 0, 00)
        self.oled.text(("OD:     " + od), 0, 10)
        self.oled.text(("Pump 1: " + p1), 0, 20)
        self.oled.text(("Pump 2: " + p2), 0, 30)
        self.oled.show()