def convert_time_into_mari_time(time):
    time_split = time.split('-')
    date = time_split[0]
    time = int(time_split[1])

    if time >= 1 and time < 7:
        return date + '-0100-0700'
    elif time >= 7 and time < 13:
        return date + '-0700-1300'
    elif time >= 13 and time < 19:
        return date + '-1300-1900'
    elif time >= 19 or time == 0:
        return date + '-1900-0100'
    else:
        return date + '-0000-0000'