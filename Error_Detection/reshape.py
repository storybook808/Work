import csv
import os
import sys

def main(argv):
    input_dir_name   = 'input'
    output_dir_name  = 'reshape'

    current_dir = os.path.dirname(os.path.abspath(__file__))

    input_dir   = os.path.join(current_dir, input_dir_name)
    output_dir  = os.path.join(current_dir, output_dir_name)

    # Scans for all CSV files within the input directory.
    for item in os.listdir(input_dir):
        if item.split('.')[len(item.split('.'))-1].lower() == 'csv':
            # Open input and output files.
            with open(os.path.join(input_dir, item)) as input_file:
                input_reader = csv.reader(input_file)
                with open(os.path.join(output_dir, item), 'wb') as output_file:
                    output_writer = csv.writer(output_file)

                    # Skips header.
                    input_reader.next()

                    output_writer.writerow(['datetime', 'sensor', 'value'])

                    for row in input_reader:
                        if row[1] != '' or row[1] != ' ':
                            output_writer.writerow([row[0], 't14', row[1]])
                        if row[2] != '' or row[2] != ' ':
                            output_writer.writerow([row[0], 't15', row[2]])
                        if row[3] != '' or row[3] != ' ':
                            output_writer.writerow([row[0], 't16', row[3]])
                        if row[4] != '' or row[4] != ' ':
                            output_writer.writerow([row[0], 't17', row[4]])
                        if row[5] != '' or row[5] != ' ':
                            output_writer.writerow([row[0], 't18', row[5]])


if __name__ == '__main__':
    main(sys.argv[1:])