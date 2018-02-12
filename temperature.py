
# Code to record readings into a file untill button is pressed.

import os
import glob
import time
import sys
import RPi.GPIO as GPIO
import json
import csv
#................................DEVICE VERSION..............................
print "\n<<<<<<<<<This code record the readings with Date and Time when Button is Pressed>>>>>>>>>>\n"
print("sys.version:")
print(sys.version + "\n")

print("GPIO.VERSION: " + GPIO.VERSION)
print("GPIO.RPI_INFO['P1_REVISION'] = " + str(GPIO.RPI_INFO['P1_REVISION']));

#...............................GPIO PINS SETUP............................
led_red = 11
led_green = 13
button = 12
GPIO.setmode(GPIO.BOARD)
GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(led_red, GPIO.OUT)
GPIO.setup(led_green, GPIO.OUT)

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'


#................................Reading Temperature.........................
def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c, temp_f


# .......................................MAIN........................................
#myrecord = dict()
file_name = "temperature.txt"
file_out = open(file_name,'w')
print("\nPress Button to Read Temperature\n")
try:
 writer = csv.writer(file_out)
 fieldnames = ('date','temperature')
 writer = csv.DictWriter(file_out, fieldnames=fieldnames,delimiter = '\t')
 headers = dict((n,n) for n in fieldnames)
 writer.writerow(headers) 
 while True:
   GPIO.output(led_red,1)
   GPIO.output(led_green,0)
   prev_input = 0
   input = GPIO.input(button)  
   while((not prev_input) and input):
    GPIO.output(led_red,0)
    GPIO.output(led_green,1)
    #print (read_temp())
    print "Recording Data Into a FILE:",file_name
    timestamp = time.strftime("%m-%d-%y-%H:%M:%S")
    cel, far = read_temp()
    writer.writerow({'date':timestamp,'temperature':cel})
    #myrecord[timestamp] = cel
    prev_input = input
   GPIO.output(led_green,0) 
    
except KeyboardInterrupt:  
 file_out.close()
 GPIO.cleanup()
GPIO.cleanup()
#..........................................END.................................

#with open(file_name,"w") as file_out:
# file_out.write(myrecord)
