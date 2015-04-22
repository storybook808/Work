__author__ = 'Steven Chen'
__email__  = 'chenstev@hawaii.edu'

from datetime_util import compare_minute
from reshape import reshape
from window import Window

import csv
import os
import shutil
import sys

def main(argv):
    # Define input, output, and archive directory names.
    turbine_dir_name = 'reshaped_turbine'
    weather_dir_name = 'raw_weather'
    archive_dir_name = 'archived'
    output_dir_name  = 'output'
    # Process raw turbine files into the eshape format.
    # [datetime, sensor id, value]
    reshape()
    # Define current working directory.
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Define input, output, and archive directories.
    turbine_dir         = os.path.join(current_dir, turbine_dir_name)
    weather_dir         = os.path.join(current_dir, weather_dir_name)
    turbine_archive_dir = os.path.join(turbine_dir, archive_dir_name)
    weather_archive_dir = os.path.join(weather_dir, archive_dir_name)
    output_dir  = os.path.join(current_dir, output_dir_name)
    # Process all of the turbine data.
    # Scan for all CSV files within the turbine data folder.
    for item in os.listdir(turbine_dir):
        if item.split('.')[-1].lower() == 'csv':
            windows = [Window('t14'), Window('t15'), Window('t16'), \
                       Window('t17'), Window('t18')]
            # Open input and output files.
            with open(os.path.join(turbine_dir, item)) as input_file:
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
                                if compare_minute(window.startTime(), row[0]) < 9:
                                    window.append(row)
                                    continue
                                if compare_minute(window.startTime(), row[0]) == 9:
                                    window.append(row)
                                    if window.size() >= 7:
                                        output_writer.writerow([window.startTime(), window.who_am_i(), window.average()])

                                if compare_minute(window.startTime(), row[0]) > 9:
                                    if window.size() >= 7:
                                        output_writer.writerow([window.startTime(), window.who_am_i(), window.average()])
                                    window.empty()
                                    window.append(row)
                                    continue
                                window.empty()
            shutil.move(os.path.join(turbine_dir, item), os.path.join(turbine_archive_dir, item))
    # Process all of the weather data.
    # Scan for all CSV files within the weather data folder.
    for item in os.listdir(weather_dir):
        if item.split('.')[-1].lower() == 'csv':
            window = Window('speed_avg')
            # Open input and output files.
            with open(os.path.join(weather_dir, item)) as input_file:
                input_reader = csv.reader(input_file)
                with open(os.path.join(output_dir, item), 'wb') as output_file:
                    output_writer = csv.writer(output_file)
                    print 'Processing ' + item
                    input_reader.next()
                    # Write header into the output file.
                    output_writer.writerow(['datetime', 'value'])
                    for row in input_reader:
                        # Add row if the buffer is empty.
                        if window.size() == 0:
                            window.append([row[0], window.who_am_i(), row[2]])
                            continue
                        if compare_minute(window.startTime(), row[0]) < 9:
                            window.append([row[0], window.who_am_i(), row[2]])
                            continue
                        if compare_minute(window.startTime(), row[0]) == 9:
                            window.append([row[0], window.who_am_i(), row[2]])
                            if window.size() >= 7:
                                output_writer.writerow([window.startTime(), window.average()])

                        if compare_minute(window.startTime(), row[0]) > 9:
                            if window.size() >= 7:
                                output_writer.writerow([window.startTime(), window.average()])
                            window.empty()
                            window.append([row[0], window.who_am_i(), row[2]])
                            continue
                        window.empty()
            shutil.move(os.path.join(weather_dir, item), os.path.join(weather_archive_dir, item))
    return 1

if __name__ == '__main__':
    main(sys.argv[1:])