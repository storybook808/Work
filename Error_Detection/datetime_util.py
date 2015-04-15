import datetime

def convert_dt(dt_string):
    date = dt_string.split(' ')[0]
    time = dt_string.split(' ')[1]

    month = int(date.split('/')[0])
    day   = int(date.split('/')[1])
    year  = int(date.split('/')[2])

    hour   = int(time.split(':')[0])
    minute = int(time.split(':')[1])

    try:
        second = int(time.split(':')[2])
    except:
        second = 0

    return datetime.datetime(year, month, day, hour, minute, second)

def compare_second(dt_string_1, dt_string_2):
    dt_1 = convert_dt(dt_string_1)
    dt_2 = convert_dt(dt_string_2)

    dt_delta = dt_2 - dt_1

    return dt_delta.total_seconds()

def compare_minute(dt_string_1, dt_string_2):
    return compare_second(dt_string_1, dt_string_2) / 60

def compare_hour(dt_string_1, dt_string_2):
    return compare_second(dt_string_1, dt_string_2) / 3600