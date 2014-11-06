import SoundLevelMeterUtility
import os
import sys

from RAW import RAWLINK
from CSV import CSVLINK
from RESHAPED import RESHAPEDLINK

#set the working directory of this script to its path directory
#this is to help crontab figure out where the supporting files are
print sys.argv[0]
if os.path.dirname(sys.argv[0]) == '':
    pass
else:
    os.chdir(os.path.dirname(sys.argv[0]))

DATETIMEFORMAT = "%d-%m-%Y %H:%M:%S"
raw_location = os.path.dirname(os.path.abspath(RAWLINK.__file__))
csv_location = os.path.dirname(os.path.abspath(CSVLINK.__file__))
reshaped_location = os.path.dirname(os.path.abspath(RESHAPEDLINK.__file__))
print "\nProcessing...\n"
print "RAW: " + str(raw_location)
print "CSV: " + str(csv_location)
print "RESHAPED: " + str(reshaped_location)
print "\nCreating SoundLevelMeter\n"

SoundLevelMeter = SoundLevelMeterUtility.SoundLevelMeterUtility(raw_location,\
    csv_location, reshaped_location, DATETIMEFORMAT, False, False, False, 10)

SoundLevelMeter.project_extract()
#SoundLevelMeter.clear_archive()
