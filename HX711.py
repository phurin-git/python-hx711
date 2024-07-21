import RPi.GPIO as GPIO
import time
class HX711:
    def __init__(self): 
        self.PD_SCK = 0
        self.DOUT = 0
        self.GAIN = 0
        self.OFFSET = 0
        self.SCALE = 1

    def begin(self, dout, pd_sck, gain = 128):
        self.PD_SCK = pd_sck
        self.DOUT = dout
        GPIO.setup(self.PD_SCK, GPIO.OUT)
        GPIO.setup(self.DOUT, GPIO.IN)
        self.set_gain(gain)
    
    def is_ready(self):
        return GPIO.input(self.DOUT) == False
        
    def wait_ready(self, delay_ms = 0):
        while(not self.is_ready()):
            time.sleep(delay_ms / 1000)

    def wait_ready_retry(self, retries = 3, delay_ms = 0):
        for i in range(retries):
            if(self.is_ready()):
                return True
            time.sleep(delay_ms / 1000)
        return False
    
    def wait_ready_timeout(self, timeout = 1000, delay_ms = 0):
        millisStarted = round(time.time() * 1000)
        while(round(time.time() * 1000) - millisStarted < timeout):
            if(self.is_ready()):
                return True
        time.sleep(delay_ms / 1000)
        return False

    def set_gain(self, gain = 128):
        if(gain == 128):
            self.GAIN = 1
        elif(gain == 64):
            self.GAIN = 3
        elif(gain == 32):
            self.GAIN = 2

    def ShiftIn(self, data, clock, order):
        value = 0
        for i in range(8):
            GPIO.output(clock, GPIO.HIGH)
            if(order == "LSBFIRST"):
                value |= GPIO.input(data) << i
            else:
                value |= GPIO.input(data) << (7 - i)
            GPIO.output(clock, GPIO.LOW)
        return value
        
    def read(self):
        self.wait_ready()
        value = 0
        filler = 0x00
        data = [0, 0, 0]
        data[2] = self.ShiftIn(self.DOUT, self.PD_SCK, "MSBFIRST")
        data[1] = self.ShiftIn(self.DOUT, self.PD_SCK, "MSBFIRST")
        data[0] = self.ShiftIn(self.DOUT, self.PD_SCK, "MSBFIRST")
        for  i in range(self.GAIN):
            GPIO.output(self.PD_SCK, GPIO.HIGH)
            GPIO.output(self.PD_SCK, GPIO.LOW)
        if(data[2] & 0x80):
            filler = 0xFF
        else:
            filler = 0x00
        value = (filler << 24
    			| data[2] << 16
    			| data[1] << 8
    			| data[0])
        return value
        
    def read_average(self, times = 10):
        sum = 0
        for i in range(times):
            sum = sum + self.read()
        time.sleep(0)
        return sum / times
        
    def get_value(self, times = 1):
        return self.read_average(times) - self.OFFSET
        
    def get_units(self, times = 1):
        return self.get_value(times) / self.SCALE

    def tare(self, times = 10):
        sum = self.read_average(times)
        self.set_offset(sum)
        
    def set_scale(self, scale = 1.0):
        self.SCALE = scale
        
    def get_scale(self):
        return self.SCALE

    def set_offset(self, offset = 0):
        self.OFFSET = offset

    def get_offset(self):
        return self.OFFSET

    def power_down(self):
        GPIO.output(self.PD_SCK, GPIO.LOW)
        GPIO.output(self.PD_SCK, GPIO.HIGH)
        
    def power_up(self):
        GPIO.output(self.PD_SCK, GPIO.LOW)
