from list_statistics import List_Statistics

import csv
import os
import sys

def main(argv):
    if len(argv) != 1:
        print 'usage: python driver.py <sample size>'
        return

    sample_size = int(argv[0])

    error_count = 0

    archive_dir_name = 'archive'
    input_dir_name   = 'input'
    output_dir_name  = 'output'

    current_dir = os.path.dirname(os.path.abspath(__file__))

    archive_dir = os.path.join(current_dir, archive_dir_name)
    input_dir   = os.path.join(current_dir, input_dir_name)
    output_dir  = os.path.join(current_dir, output_dir_name)

    # Scans for all CSV files within the input directory.
    for item in os.listdir(input_dir):
        if item.split('.')[len(item.split('.'))-1].lower() == 'csv':
            # Blanks buffer for rolling standard deviation.
            date_time = []
            # t14
            sensor_1  = List_Statistics([])
            # t15
            sensor_2  = List_Statistics([])
            # t16
            sensor_3  = List_Statistics([])
            # t17
            sensor_4  = List_Statistics([])
            # t18
            sensor_5  = List_Statistics([])

            # Open input and output files.
            with open(os.path.join(input_dir, item)) as input_file:
                input_reader = csv.reader(input_file)
                with open(os.path.join(output_dir, item)) as output_file:
                    output_writer = csv.writer(output_file)

                    # Write header into the output file.
                    output_writer.writerow(input_reader.next())

                    for row in input_reader:
                        # If the current row is incomplete.
                        if len(row) != 6:
                            # Update error counter.
                            error_count = error_count + 1
                            print 'Error ' + error_count ': ' + row[0]
                            continue

                        # If the rolling standard deviation window is empty,
                        # then load a row of data into the window.
                        if date_time.count == 0:
                            date_time.append(row[0])
                            sensor_1.append(row[1])
                            sensor_2.append(row[2])
                            sensor_3.append(row[3])
                            sensor_4.append(row[4])
                            sensor_5.append(row[5])
                            continue



if __name__ == '__main__':
    main(sys.argv[1:])