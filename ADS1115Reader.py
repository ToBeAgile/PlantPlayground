import Adafruit_ADS1x15

class ADS1115Reader:
    
    adc = Adafruit_ADS1x15.ADS1115()
    GAIN = 16

    def reader(self, channel):
        value = self.adc.read_adc_difference(channel, gain=self.GAIN, data_rate=8)
        return value