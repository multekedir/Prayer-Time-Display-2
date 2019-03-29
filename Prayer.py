import praytimes as pt
import requests
import re
from datetime import date, datetime


#---------------------- prayTimes Object -----------------------

timeNames = ['fajr', 'dhuhr', 'asr', 'maghrib', 'isha']
new_iqama = ['+1', '+0', '+0', '+0', '+60']


longitude= 45.562015
latitude= -122.865750
calculation= 'ISNA'
daylight_savings= 1

prayTimes = pt.PrayTimes(calculation);

def get_prayertime(prayer):
        """
        get the time of Athan from the prayer_api.py file.
        Location is set to Eugene,OR. Can be changed by
        adjusting the long, lat and elevation.
        :param prayer: enter a prayer from one the list [fajr, sunrise, dhuhr, asr, maghrib, isha]
        :param format: adjust time format in '12h' or '24h'
        :return: Time of prayer
        """


        times = prayTimes.getTimes(date.today(), (longitude, latitude), -8, daylight_savings)

        return datetime.strptime(times[prayer], "%H:%M").strftime("%I:%M %p")

def read_data(url):
    new_data = []
    print("Data file url =", url)
    r = requests.get(url, stream=True)
    for line in r.iter_lines():
        if line:
            new_data.append(str(line.decode('utf-8')).rstrip('\n'))
    return new_data

def check_addition(input):
    if (len(input) == 2):
        return bool(re.match("\+[0-9]",input))
    else:
        return bool(re.match("\+([0-5])([0-9])",input))

def check_phone(input):
    return bool(bool(re.fullmatch("1[0-2]|0[1-9]:[0-5][0-9] ?[AaPp][Mm]", input)))

def validate(data):
    print("Valid check data =", data)
    result = []
    for i  in data:
        print("Valid check for =", i)
        if i.startswith('+'):
            result.append(check_addition(i))
        else:
            result.append(check_phone(i))
        print("Valid check =", result)
    return all(result) and len(result) == 5

def save_data(func, names):
    if validate([func(i) for i in names]):
        myfile =  open("./static/iqama.txt", "w")
        for i in names:
            myfile.write(func(i)+'\n')

        myfile.close()
        return True
    else:
        return False



def set_iqama(iqama, data_file):
    print("Data from file =", read_data(data_file))
    global new_iqama
    new_iqama=iqama

def cal_iqama_time(hour, difference):

    """
    Gets prayer time and split the string and add
    the min to the prayer time.
    If hour 11:50am and difference is 20 -> 12:10pm
    :param hour: 11:50pm
    :param difference: 20
    :return: time in 12hr formats
    """
    #'05:34 AM'
    period = hour[-2:]  # get the am and pm
     # get the time
     # hour = 05, min =34
    hour, min = hour.strip('AM,PM, ').split(':')
    iqama_min = int(min) + difference
    # check if it is more than 59 min
    if iqama_min >= 60:
        iqama_min -= 60
        iqama_hour = int(hour) + 1

        if (len(str(iqama_min)) == 1):
            #make it to 00:00 format
            iqama_min = '0' + str(iqama_min)

        if (len(str(iqama_hour)) == 1):
            #make it to 00:00 format
            iqama_hour = '0' + str(iqama_hour)

        #check time change AM to PM and PM to AM
        if hour == '11':
            if period == "AM":
                period = 'PM'
            elif period == 'PM':
                period = 'AM'

        return str(iqama_hour) + ":" + str(iqama_min) + " "+ period
    return str(hour) + ":" + str(iqama_min) +  " "+period

def get_iqamatime(prayer, datain):

    """
    Check id input is a static or an addition.
    user input can start with '+' or a static time '5:25 PM'
    calls prayer_api.py
    :return: static time ('4:30 PM') or adds the time from Athan api
    """

    time = get_prayertime(prayer)
    if datain.startswith('+'):
        datain.strip('+')
        try:
            datain = int(datain)
        except ValueError:
            print("Oops!  That was no valid number.  Try again...")
        else:
            iqama = cal_iqama_time(time,datain)
            return iqama
    elif (("pm" or "am" and ":" in datain) and (len(datain) > 6)):
        return datain
    return "ERROR"


def map_prayerdata(url):
    new_iqama = read_data(url)
    p_times = list(map(get_prayertime,timeNames))
    i_times = list(map(get_iqamatime, *(timeNames, new_iqama)))
    print('*'*100)
    print("Prayer Times =", p_times)
    print("Prayer Times =", i_times)
    print("change =", new_iqama)
    data = dict(zip(timeNames, list(zip(p_times,i_times))))
    print('Prayer Data = ',data)
    print('*'*100)
    return data
