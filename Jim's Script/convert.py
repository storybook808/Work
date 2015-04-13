# -*- coding: utf-8 -*-
"""
Created on Thu Feb 05 15:34:57 2015

@author: Steven Chen
"""

import csv
import os

# Target current directory
directory_target = os.listdir(os.path.dirname(os.path.abspath(__file__)))

# Initialize count variables
count_total = 0
count_write = 0

# Scroll through every item in current working directory
for item in directory_target:
    # Parse the file name for the extension
    item_target = item.split(".")
    # Target the extension of the file name
    extension_target = item_target[len(item_target)-1]
    # Check if the extension for CSV or csv file type
    if extension_target == "CSV" or extension_target == "csv":
        # Open target file to read
        with open(item, "r") as data_file:
            # Open target file with a CSV reader
            data_reader = csv.reader(data_file)
            # Disregard the header
            data_reader.next()
            # Scroll through every item in current CSV file
            for row in data_reader:
                # Increment counter for each row present
                count_total = count_total+1
                # Parse the row for each column
                row_target = row.split(",")
                # Check row for a valid amount of columns
                if len(row_target) < 6:
                    #
                    print row_target[0] + " is not valid!"
                    # Missing too much information, skip to the next row
                    continue
