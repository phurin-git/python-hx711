# Load Cell Calibration
from HX711 import HX711
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
scale = HX711()
calibration_factor = 529 #-7050 worked for my 440lb max scale setup
def setup(obj):
    obj.begin(21,23) 
    obj.set_scale()
    obj.tare()   #Reset the scale to 0  
    zero_factor = obj.read_average() #Get a baseline reading
    print("Zero factor: " + str(zero_factor)) #This can be used to remove the need to tare the scale. Useful in permanent scale projects.
    scale.set_scale(calibration_factor) #Adjust to this calibration factor
    
setup(scale)
while(True):
    weight = scale.get_units()
    if(weight <= 0):
        weight = 0
    print("Reading: " + str(weight) + " g")

