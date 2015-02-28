import NISignalExpressUtility
import os
from DataFiles import __data__
from ConvertedCSVs import __converted__
from ReshapedCSVs import __reshaped__
from CalibratedCSVs import __calibrated__

data_location = os.path.dirname(os.path.abspath(__data__.__file__))
converted_location = os.path.dirname(os.path.abspath(__converted__.__file__))
reshaped_location = os.path.dirname(os.path.abspath(__reshaped__.__file__))
calibrated_location = os.path.dirname(os.path.abspath(__calibrated__.__file__))

print "data: ", data_location
print "converted: ", converted_location
print "reshaped: ", reshaped_location
print "calibrated: ", calibrated_location

data_folders_locations = []
for folder_name in os.listdir(data_location):
    if ".py" not in folder_name:
        data_folders_locations.append(os.path.join(data_location, folder_name))
#        print data_folders_locations


for data_folders in data_folders_locations:
    print data_folders
    NIExtract = NISignalExpressUtility.NISignalExpressUtility(\
        data_folders, converted_location,\
        reshaped_location, calibrated_location)
    NIExtract.convert_to_csv()
    NIExtract.reshape_csv()
    NIExtract.calibrate_output()
