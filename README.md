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

## Features
1. It provides a `tare()` function, which "resets" the scale to 0. Many other
   implementations calculate the tare weight when the ADC is initialized only.
   I needed a way to be able to set the tare weight at any time.
   **Use case**: Place an empty container on the scale, call `tare()` to reset
   the readings to 0, fill the container and get the weight of the content.

2. It provides a `power_down()` function, to put the ADC into a low power mode.
   According to the datasheet,
   > When PD_SCK pin changes from low to high and stays at high
   > for longer than 60μs, HX711 enters power down mode.

   **Use case**: Battery-powered scales. Accordingly, there is a `power_up()`
   function to get the chip out of the low power mode.

3. It has a `set_gain(byte gain)` function that allows you to set the gain factor
   and select the channel. According to the datasheet,
   > Channel A can be programmed with a gain of 128 or 64, corresponding to
   a full-scale differential input voltage of ±20mV or ±40mV respectively, when
   a 5V supply is connected to AVDD analog power supply pin. Channel B has
   a fixed gain of 32.

   The same function is used to select the channel A or channel B, by passing
   128 or 64 for channel A, or 32 for channel B as the parameter. The default
   value is 128, which means "channel A with a gain factor of 128", so one can
   simply call `set_gain()`.

   This function is also called from the initializer method `begin()`.

4. The `get_value()` and `get_units()` functions can receive an extra parameter "times",
   and they will return the average of multiple readings instead of a single reading.


## How to calibrate your load cell
1. Call `set_scale()` with no parameter.
2. Call `tare()` with no parameter.
3. Place a known weight on the scale and call `get_units(10)`.
4. Divide the result in step 3 to your known weight. You should
   get about the parameter you need to pass to `set_scale()`.
5. Adjust the parameter in step 4 until you get an accurate reading.

## Credits

Thanks to [Weihong Guan](https://github.com/aguegu) who started the first version of this library in 2012 (see [ardulibs](https://github.com/aguegu/ardulibs/tree/master/hx711)) and [Bogdan Necula](https://github.com/bogde) (see [bodge](https://github.com/bogde/HX711)) who took over in 2014 and others who contributed to this library. Thanks for your hard work! (This python version developed by me in 2021)