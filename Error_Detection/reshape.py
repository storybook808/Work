import csv
import os
import shutil

def reshape():
    input_dir_name   = 'input'
    archive_dir_name = 'archived'
    output_dir_name  = 'reshaped'

    current_dir = os.path.dirname(os.path.abspath(__file__))

    input_dir   = os.path.join(current_dir, input_dir_name)
    archive_dir = os.path.join(input_dir, archive_dir_name)
    output_dir  = os.path.join(current_dir, output_dir_name)

    # Scans for all CSV files within the input directory.
    for item in os.listdir(input_dir):
        if item.split('.')[len(item.split('.'))-1].lower() == 'csv':
            # Open input and output files.
            with open(os.path.join(input_dir, item)) as input_file:
                input_reader = csv.reader(input_file)
                with open(os.path.join(output_dir, item), 'wb') as output_file:
                    output_writer = csv.writer(output_file)
                    print 'Reshaping ' + item
                    # Skips header.
                    input_reader.next()
                    # Write new header.
                    output_writer.writerow(['datetime', 'sensor', 'value'])
                    # Rearrange values into the reshape format.
                    for row in input_reader:
                        if row[1] != '' and row[1] != ' ':
                            output_writer.writerow([row[0], 't14', row[1]])
                        if row[2] != '' and row[2] != ' ':
                            output_writer.writerow([row[0], 't15', row[2]])
                        if row[3] != '' and row[3] != ' ':
                            output_writer.writerow([row[0], 't16', row[3]])
                        if row[4] != '' and row[4] != ' ':
                            output_writer.writerow([row[0], 't17', row[4]])
                        if row[5] != '' and row[5] != ' ':
                            output_writer.writerow([row[0], 't18', row[5]])
            # Move input file to archive directory.
            shutil.move(os.path.join(input_dir, item), os.path.join(archive_dir, item))
