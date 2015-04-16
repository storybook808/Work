__author__ = 'Steven Chen'
__email__  = 'chenstev@hawaii.edu'

from datetime_util import compare_hour
from reshape import reshape
from window import Window

import csv
import os
import shutil
import sys

def main(argv):
    # Define input, output, and archive directory names.    
    input_dir_name   = 'reshaped'
    archive_dir_name = 'archived'
    output_dir_name  = 'output'    
    # Must have two input parameters.
    if len(argv) != 2:
        print 'usage: driver.py <sample size (hours)> <threshold for std>'
        return
    # Save the input parameters.
    sample_size = int(argv[0])
    threshold   = int(argv[1])
    # Process raw data files into the eshape format. 
    # [datetime, sensor id, value]
    reshape()
    # Define current working directory.
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Define input, output, and archive directories
    input_dir   = os.path.join(current_dir, input_dir_name)
    archive_dir = os.path.join(input_dir, archive_dir_name)
    output_dir  = os.path.join(current_dir, output_dir_name)
    # Scans for all CSV files within the input directory.
    for item in os.listdir(input_dir):
        if item.split('.')[len(item.split('.'))-1].lower() == 'csv':
            
            windows = [Window('t14'), Window('t15'), Window('t16'), \
                       Window('t17'), Window('t18')]

            # Open input and output files.
            with open(os.path.join(input_dir, item)) as input_file:
                input_reader = csv.reader(input_file)
                with open(os.path.join(output_dir, item), 'wb') as output_file:
                    output_writer = csv.writer(output_file)
                    print 'Processing ' + item
                    # Write header into the output file.
                    output_writer.writerow(input_reader.next())
                    for row in input_reader:
                        for window in windows:
                            if row[1] == window.who_am_i():
                                # Add row if the buffer is empty.
                                if window.size() == 0:
                                    window.append(row)
                                    continue
                                # Add rows until the buffer contains points
                                # within the window size.
                                if compare_hour(window.startTime(), row[0]) < sample_size:
                                    window.append(row)
                                    continue
                                # Grow the buffer if the std is below
                                # threshold. This is to capture ranges of bad
                                # data that could be larger than the window.
                                # Otherwise, pop the first item off and write
                                # it to the output file and shift the window.
                                if window.std() > threshold:
                                    output_writer.writerow(window.pop(0))
                                    window.append(row)
                                    continue
                                window.append(row)
                                if window.std() > threshold:
                                    print 'Sensor ' + window.who_am_i()
                                    print 'Standard deviation below threshold...'
                                    print 'Discarding ' + str(window.size()) + ' items...'
                                    print 'Starting from ' + window.startTime() + ' and ending on ' + window.endTime()
                                    window.empty()
                                    window.append(row)
                    # Check to see if the remaining items are within the
                    # threshold of good data.
                    for window in windows:
                        if window.std() > threshold:
                            while window.size() != 0:
                                output_writer.writerow(window.pop(0))
                        else:
                            print 'Sensor ' + window.who_am_i()
                            print 'Standard deviation below threshold...'
                            print 'Discarding ' + str(window.size()) + ' items...'
                            print 'Starting from ' + window.startTime() + ' and ending on ' + window.endTime()
            # Move input file to archive directory.
            shutil.move(os.path.join(input_dir, item), os.path.join(archive_dir, item))

if __name__ == '__main__':
    main(sys.argv[1:])