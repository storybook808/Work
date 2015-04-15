from datetime_util import compare_minute
from list_statistics import List_Statistics
from reshape import reshape

import csv
import os
import shutil
import sys

def main(argv):
    # Must have two input parameters.
    if len(argv) != 2:
        print 'usage: python driver.py <sample size> <threshold)'
        return

    sample_size = int(argv[0])
    threshold   = int(argv[1])

    # Process raw data files into the eshape format.
    reshape()

    input_dir_name   = 'reshaped'
    archive_dir_name = 'archived'
    output_dir_name  = 'output'

    current_dir = os.path.dirname(os.path.abspath(__file__))

    input_dir   = os.path.join(current_dir, input_dir_name)
    archive_dir = os.path.join(input_dir, archive_dir_name)
    output_dir  = os.path.join(current_dir, output_dir_name)

    # Scans for all CSV files within the input directory.
    for item in os.listdir(input_dir):
        if item.split('.')[len(item.split('.'))-1].lower() == 'csv':
            # Blanks buffer for rolling standard deviation.
            # t14
            date_time_1 = []
            sensor_1 = List_Statistics([])
            # t15
            date_time_2 = []
            sensor_2 = List_Statistics([])
            # t16
            date_time_3 = []
            sensor_3 = List_Statistics([])
            # t17
            date_time_4 = []
            sensor_4 = List_Statistics([])
            # t18
            date_time_5 = []
            sensor_5 = List_Statistics([])
            # Open input and output files.
            with open(os.path.join(input_dir, item)) as input_file:
                input_reader = csv.reader(input_file)
                with open(os.path.join(output_dir, item), 'wb') as output_file:
                    output_writer = csv.writer(output_file)
                    print 'Processing ' + item
                    # Write header into the output file.
                    output_writer.writerow(input_reader.next())
                    for row in input_reader:
                        if row[1] == 't14':
                            # Add row if the buffer is empty.
                            if len(date_time_1) == 0:
                                date_time_1.append(row[0])
                                sensor_1.append(int(row[2]))
                            else:
                                # Add rows until the buffer contains points
                                # within the window size.
                                if compare_minute(date_time_1[0], row[0]) < sample_size:
                                    date_time_1.append(row[0])
                                    sensor_1.append(int(row[2]))
                                else:
                                    # Grow the buffer if the std is below
                                    # threshold. This is to capture ranges of
                                    # bad data that could be larger than the
                                    # window. Otherwise, pop the first item off
                                    # and write it to the output file and shift
                                    # the window.
                                    if sensor_1.std() > threshold:
                                        output_writer.writerow([date_time_1.pop(0), 't14', sensor_1.pop(0)])
                                        date_time_1.append(row[0])
                                        sensor_1.append(int(row[2]))
                                    else:
                                        date_time_1.append(row[0])
                                        sensor_1.append(int(row[2]))
                                        if sensor_1.std() <= threshold:
                                            continue
                                        else:
                                            print 'Sensor t14'
                                            print 'Standard deviation below threshold...'
                                            print 'Discarding ' + str(len(date_time_1)) + ' items...'
                                            print 'Starting from ' + date_time_1[0] + ' and ending on ' + date_time_1[-1]
                                            date_time_1 = [row[0]]
                                            sensor_1 = List_Statistics([int(row[2])])

                        elif row[1] == 't15':
                            # Add row if the buffer is empty.
                            if len(date_time_2) == 0:
                                date_time_2.append(row[0])
                                sensor_2.append(int(row[2]))
                            else:
                                # Add rows until the buffer contains points
                                # within the window size.
                                if compare_minute(date_time_2[0], row[0]) < sample_size:
                                    date_time_2.append(row[0])
                                    sensor_2.append(int(row[2]))
                                else:
                                    # Grow the buffer if the std is below
                                    # threshold. This is to capture ranges of
                                    # bad data that could be larger than the
                                    # window. Otherwise, pop the first item off
                                    # and write it to the output file and shift
                                    # the window.
                                    if sensor_2.std() > threshold:
                                        output_writer.writerow([date_time_2.pop(0), 't15', sensor_2.pop(0)])
                                        date_time_2.append(row[0])
                                        sensor_2.append(int(row[2]))
                                    else:
                                        date_time_2.append(row[0])
                                        sensor_2.append(int(row[2]))
                                        if sensor_2.std() <= threshold:
                                            continue
                                        else:
                                            print 'Sensor t15'
                                            print 'Standard deviation below threshold...'
                                            print 'Discarding ' + str(len(date_time_2)) + ' items...'
                                            print 'Starting from ' + date_time_2[0] + ' and ending on ' + date_time_2[-1]
                                            date_time_2 = [row[0]]
                                            sensor_2 = List_Statistics([int(row[2])])
                        elif row[1] == 't16':
                            # Add row if the buffer is empty.
                            if len(date_time_3) == 0:
                                date_time_3.append(row[0])
                                sensor_3.append(int(row[2]))
                            else:
                                # Add rows until the buffer contains points
                                # within the window size.
                                if compare_minute(date_time_3[0], row[0]) < sample_size:
                                    date_time_3.append(row[0])
                                    sensor_3.append(int(row[2]))
                                else:
                                    # Grow the buffer if the std is below
                                    # threshold. This is to capture ranges of
                                    # bad data that could be larger than the
                                    # window. Otherwise, pop the first item off
                                    # and write it to the output file and shift
                                    # the window.
                                    if sensor_3.std() > threshold:
                                        output_writer.writerow([date_time_3.pop(0), 't16', sensor_3.pop(0)])
                                        date_time_3.append(row[0])
                                        sensor_3.append(int(row[2]))
                                    else:
                                        date_time_3.append(row[0])
                                        sensor_3.append(int(row[2]))
                                        if sensor_3.std() <= threshold:
                                            continue
                                        else:
                                            print 'Sensor t16'
                                            print 'Standard deviation below threshold...'
                                            print 'Discarding ' + str(len(date_time_3)) + ' items...'
                                            print 'Starting from ' + date_time_3[0] + ' and ending on ' + date_time_3[-1]
                                            date_time_3 = [row[0]]
                                            sensor_3 = List_Statistics([int(row[2])])
                        elif row[1] == 't17':
                            # Add row if the buffer is empty.
                            if len(date_time_4) == 0:
                                date_time_4.append(row[0])
                                sensor_4.append(int(row[2]))
                            else:
                                # Add rows until the buffer contains points
                                # within the window size.
                                if compare_minute(date_time_4[0], row[0]) < sample_size:
                                    date_time_4.append(row[0])
                                    sensor_4.append(int(row[2]))
                                else:
                                    # Grow the buffer if the std is below
                                    # threshold. This is to capture ranges of
                                    # bad data that could be larger than the
                                    # window. Otherwise, pop the first item off
                                    # and write it to the output file and shift
                                    # the window.
                                    if sensor_4.std() > threshold:
                                        output_writer.writerow([date_time_4.pop(0), 't17', sensor_4.pop(0)])
                                        date_time_4.append(row[0])
                                        sensor_4.append(int(row[2]))
                                    else:
                                        date_time_4.append(row[0])
                                        sensor_4.append(int(row[2]))
                                        if sensor_4.std() <= threshold:
                                            continue
                                        else:
                                            print 'Sensor t17'
                                            print 'Standard deviation below threshold...'
                                            print 'Discarding ' + str(len(date_time_4)) + ' items...'
                                            print 'Starting from ' + date_time_4[0] + ' and ending on ' + date_time_4[-1]
                                            date_time_4 = [row[0]]
                                            sensor_4 = List_Statistics([int(row[2])])
                        elif row[1] == 't18':
                            # Add row if the buffer is empty.
                            if len(date_time_5) == 0:
                                date_time_5.append(row[0])
                                sensor_5.append(int(row[2]))
                            else:
                                # Add rows until the buffer contains points
                                # within the window size.
                                if compare_minute(date_time_5[0], row[0]) < sample_size:
                                    date_time_5.append(row[0])
                                    sensor_5.append(int(row[2]))
                                else:
                                    # Grow the buffer if the std is below
                                    # threshold. This is to capture ranges of
                                    # bad data that could be larger than the
                                    # window. Otherwise, pop the first item off
                                    # and write it to the output file and shift
                                    # the window.
                                    if sensor_5.std() > threshold:
                                        output_writer.writerow([date_time_5.pop(0), 't18', sensor_5.pop(0)])
                                        date_time_5.append(row[0])
                                        sensor_5.append(int(row[2]))
                                    else:
                                        date_time_5.append(row[0])
                                        sensor_5.append(int(row[2]))
                                        if sensor_5.std() <= threshold:
                                            continue
                                        else:
                                            print 'Sensor t18'
                                            print 'Standard deviation below threshold...'
                                            print 'Discarding ' + str(len(date_time_5)) + ' items...'
                                            print 'Starting from ' + date_time_5[0] + ' and ending on ' + date_time_5[-1]
                                            date_time_5 = [row[0]]
                                            sensor_5 = List_Statistics([int(row[2])])
                        else:
                            print 'Error: Sensor not found.'

                    # Check to see if the remaining items are within the
                    # threshold of good data.
                    if sensor_1.std() > threshold:
                        while len(date_time_1) != 0:
                            output_writer.writerow([date_time_1.pop(0), 't14', sensor_1.pop(0)])
                    else:
                        print 'Sensor t14'
                        print 'Standard deviation below threshold...'
                        print 'Discarding ' + str(len(date_time_1)) + ' items...'
                        print 'Starting from ' + date_time_1[0] + ' and ending on ' + date_time_1[-1]

                    if sensor_2.std() > threshold:
                        while len(date_time_2) != 0:
                            output_writer.writerow([date_time_2.pop(0), 't15', sensor_2.pop(0)])
                    else:
                        print 'Sensor t15'
                        print 'Standard deviation below threshold...'
                        print 'Discarding ' + str(len(date_time_2)) + ' items...'
                        print 'Starting from ' + date_time_2[0] + ' and ending on ' + date_time_2[-1]

                    if sensor_3.std() > threshold:
                        while len(date_time_3) != 0:
                            output_writer.writerow([date_time_3.pop(0), 't16', sensor_3.pop(0)])
                    else:
                        print 'Sensor t16'
                        print 'Standard deviation below threshold...'
                        print 'Discarding ' + str(len(date_time_3)) + ' items...'
                        print 'Starting from ' + date_time_3[0] + ' and ending on ' + date_time_3[-1]

                    if sensor_4.std() > threshold:
                        while len(date_time_4) != 0:
                            output_writer.writerow([date_time_4.pop(0), 't17', sensor_4.pop(0)])
                    else:
                        print 'Sensor t17'
                        print 'Standard deviation below threshold...'
                        print 'Discarding ' + str(len(date_time_4)) + ' items...'
                        print 'Starting from ' + date_time_4[0] + ' and ending on ' + date_time_4[-1]

                    if sensor_5.std() > threshold:
                        while len(date_time_5) != 0:
                            output_writer.writerow([date_time_5.pop(0), 't18', sensor_5.pop(0)])
                    else:
                        print 'Sensor t18'
                        print 'Standard deviation below threshold...'
                        print 'Discarding ' + str(len(date_time_5)) + ' items...'
                        print 'Starting from ' + date_time_5[0] + ' and ending on ' + date_time_5[-1]

            # Move input file to archive directory.
            shutil.move(os.path.join(input_dir, item), os.path.join(archive_dir, item))

if __name__ == '__main__':
    main(sys.argv[1:])