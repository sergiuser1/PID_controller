import machine
from math import floor

class OD :

    odpin = machine.ADC(machine.Pin(34))
    odpin.atten(3)
    odpin.width(machine.ADC.WIDTH_10BIT)

    numSamples = 30

    def rawRead (self):
        rawData = []

        # Collect Samples
        for i in range (self.numSamples):
            rawData.append(self.odpin.read())

        # Select 5 median samples
        rawData.sort()
        medians = []
        for i in range (5):
            medians.append(rawData[floor(len (rawData)/2)])
            del rawData[floor(len (rawData)/2)]

        # Average medians
        avgRead = sum(medians)/len(medians)

        return avgRead

    def printRaw (self):
        print ("Raw input: " + str(self.rawRead()))