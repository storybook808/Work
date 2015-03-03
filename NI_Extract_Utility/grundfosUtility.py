import copy
import csv
import os
from CalibratedCSVs import __calibrated__
from Output import __output__

"""
Engineering Notes:

[#1] VFS 1-20
================================================================================
ai0 : temperature sensor
ai1 : flow sensor

Input File
================================================================================
Datetime Stamp, Sensor ID, Value, Comments

Output File
================================================================================
Datetime Stamp, Sensor ID, Value, Comments, Converted Value
"""

#Edit following paths upon folder changes
#===============================================================================
#Input folder
input_location = os.path.dirname(os.path.abspath(__calibrated__.__file__))
#Output folder
output_location = os.path.dirname(os.path.abspath(__output__.__file__))
#===============================================================================


def convert_flow(voltage):
    """
    Input(s):
    @voltage: (int/float) The output voltage from the Grundfos sensor
        
    Returns: (float) The flow rate in l/min

    Notes:
    Computes the l/min:
        flow_rate = 6.6522 x output_voltage - 2.5396

    This equation was derived from experiments to measure the accuracy of the sensor

    The ideal equation provided by the company is:
        flow_rate = (187/30) x voltage - (109/60)
    """
    return 6.6522*float(voltage)-2.5396

def convert_temperature(voltage):
    """
    Input(s):
    @voltage: (int/float) The output voltage from the Grundfos sensor
        
    Returns: (float) The temperature in Fahrenheit

    Notes:
    Computes the ideal temperature:
        temperature = (100/3) x output_voltage - (100/6)
    """
    return celsius_fahrenheit((100.0/3.0)*float(voltage)-(100.0/6.0))

def celsius_fahrenheit(temperature):
    """
    Input(s):
    @temperature: (int/float) Temperature in Celsius
        
    Returns: (float) The temperature in Fahrenheit

    Notes:
    Converts from Celsius to Fahrenheit
        F = (9/5) x C + 32
    """
    return (9.0/5.0)*temperature+32.0

#Print target locations
print "Input:\t", input_location
print "Output:\t", output_location
#Print the start message
print "\nStarting conversion...\n"
#Initialize error count
error_count = 0
#Initialize data point count
data_count = 0
#Tranverse through every item in current input data location
for item in os.listdir(input_location):
    #Parse the file name for the extension
    item_target = item.split(".")
    #Target the extension of the file name
    extension_target = item_target[len(item_target)-1]
    #Check if the extension is a CSV type file
    if extension_target == "CSV" or extension_target == "csv":
        #Provide feedback on what file is being accessed
        print "Input File:\t", item
        #Clear the output filename
        output = "";
        #Create output file name
        for part in item_target:
            #Reconstruct the file name
            if part != extension_target:
                output = output + part
            #Insert the output tag and finalize the file name
            else:
                output = output + "_output." + extension_target
        #Provide feedback on what file is being generated
        print "Output File:\t", output
        #Generate a path to the output file
        output_path = os.path.join(output_location, output)
        #Open the output file
        with open(output_path, "wb") as output_file:
            #Open output file with a CSV writer
            output_writer = csv.writer(output_file)
            #Generate a path to the input file
            item_path = os.path.join(input_location, item)
            #Open the input file
            with open(item_path, "r") as item_file:
                #Open input file with a CSV reader
                item_reader = csv.reader(item_file)
                #Skip the header
                item_reader.next()
                #Tranverse through the rows in the input file
                for row in item_reader:
                    #Clear the output buffer
                    output_buffer = []
                    #Copy the contains of the current row to the buffer
                    output_buffer = copy.deepcopy(row)

                    #Edit following list when adding more sensors
                    #===========================================================
                    #[#1] VFS 1-20 temperature sensor
                    if row[1] == "ai0":
                        output_buffer.append(convert_temperature(row[2]))
                    #[#1] VFS 1-20 Flow sensor
                    elif row[1] == "ai1":
                        output_buffer.append(convert_flow(row[2]))
                    #No sensor information can be found, skip to the next row
                    else:
                        #Increment error count
                        error_count = error_count + 1
                        continue
                    #===========================================================

                    #Increment data point count
                    data_count = data_count + 1
                    #Write new row into output file
                    output_writer.writerow(output_buffer)
#Conversion complete, report data to the user
print "\nConversion completed...\n"
print "Number of data points: ", data_count
print "Number of errors: ", error_count
