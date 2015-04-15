__author__ = 'Steven Chen'
__email__  = 'chenstev@hawaii.edu'

import datetime

# Given : @dt_string: A datetime string in the format of...
#         MM/DD/YYYY HH:MM:SS or
#         MM/DD/YYYY HH:MM
# Return: A datetime object.
def convert_dt(dt_string):
    # Parse datetime string into different sections.
    date = dt_string.split(' ')[0]
    time = dt_string.split(' ')[1]
    # Date.
    month = int(date.split('/')[0])
    day   = int(date.split('/')[1])
    year  = int(date.split('/')[2])
    # Time.
    hour   = int(time.split(':')[0])
    minute = int(time.split(':')[1])
    # If there is no seconds to parse from, then set it to 0.
    try:
        second = int(time.split(':')[2])
    except:
        second = 0
    # Generate and return a datetime object.
    return datetime.datetime(year, month, day, hour, minute, second)

# Given: @dt_string_X: Two datetime strings in the format of...
#         MM/DD/YYYY HH:MM:SS or
#         MM/DD/YYYY HH:MM
# Return: Difference between the second and first datetime strings in seconds.
def compare_second(dt_string_1, dt_string_2):
    # Convert datetime strings into datetime objects.
    dt_1 = convert_dt(dt_string_1)
    dt_2 = convert_dt(dt_string_2)
    # Create a delta object of the different between datetime 2 and 1.
    dt_delta = dt_2 - dt_1
    # Return the difference in seconds.
    return dt_delta.total_seconds()

# Given: @dt_string_X: Two datetime strings in the format of...
#         MM/DD/YYYY HH:MM:SS or
#         MM/DD/YYYY HH:MM
# Return: Difference between the second and first datetime strings in minutes.
def compare_minute(dt_string_1, dt_string_2):
    # Compute the different in seconds, then convert to minutes.
    return compare_second(dt_string_1, dt_string_2) / 60.0

# Given: @dt_string_X: Two datetime strings in the format of...
#         MM/DD/YYYY HH:MM:SS or
#         MM/DD/YYYY HH:MM
# Return: Difference between the second and first datetime strings in hours.
def compare_hour(dt_string_1, dt_string_2):
    # Compute the different in seconds, then convert to hours.
    return compare_second(dt_string_1, dt_string_2) / 3600.0