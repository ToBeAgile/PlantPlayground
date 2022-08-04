import config_dac
import RPi.GPIO as GPIO


#channel_A   = 0x30
#channel_B   = 0x34

DAC_Value_MAX = 65535

DAC_VREF = 3.3

class DAC8532:
    channel_A   = 0x30
    channel_B   = 0x34

    def __init__(self):
        self.cs_pin = config_dac.CS_DAC_PIN
        config_dac.module_init()
        
    
    def DAC8532_Write_Data(self, Channel, Data):
        config_dac.digital_write(self.cs_pin, GPIO.LOW)#cs  0
        config_dac.spi_writebyte([Channel, Data >> 8, Data & 0xff])
        config_dac.digital_write(self.cs_pin, GPIO.HIGH)#cs  0
        
    def DAC8532_Out_Voltage(self, Channel, Voltage):
        if((Voltage <= DAC_VREF) and (Voltage >= 0)):
            temp = int(Voltage * DAC_Value_MAX / DAC_VREF)
            self.DAC8532_Write_Data(Channel, temp)
  
### END OF FILE ###

