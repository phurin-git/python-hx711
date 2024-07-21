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
