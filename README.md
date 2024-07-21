# Python HX711 Library

This repository provides a Python library for interfacing with the HX711 load cell amplifier. Traditionally, HX711 sensors have official libraries available only in C++ for Arduino. This library aims to fill that gap by offering a Python implementation, making it compatible with platforms such as the Jetson Nano that use Python GPIO for sensor integration.
## Example

```python
# Load Cell Calibration
from HX711 import HX711
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
scale = HX711()
calibration_factor = 1
realweight = 0
def setup(obj):
    global realweight
    obj.begin(21,23) 
    obj.set_scale()
    obj.tare()   #Reset the scale to 0  
    zero_factor = obj.read_average() #Get a baseline reading
    print("Zero factor: " + str(zero_factor)) #This can be used to remove the need to tare the scale. Useful in permanent scale projects.
    input("Did you put your object on weight scale yet?")
    realweight = float(input("Please input real weight(g).\n"))
    
setup(scale)
while(True):
    scale.set_scale(calibration_factor) #Adjust to this calibration factor
    weight = scale.get_units()
    print("Reading: " + str(weight) + " g Calibrate Factor : " + str(calibration_factor))
    if(weight <= 0):
        weight = 0
    if(weight < (realweight - 1)):
        calibration_factor -= 1
    elif(weight > (realweight + 1)):
        calibration_factor  += 1
    else:
        break
    if(calibration_factor <= 0):
        calibration_factor = 1
```


## Credits

Thanks to [Weihong Guan](https://github.com/aguegu) who started the first version of this library in 2012 (see [ardulibs](https://github.com/aguegu/ardulibs/tree/master/hx711)) and [Bogdan Necula](https://github.com/bogde) (see [bodge](https://github.com/bogde/HX711)) who took over in 2014 and others who contributed to this library. Thanks for your hard work! (This version developed by me in 2021)