from flask import Flask, url_for, render_template, request
import praytimes as pt
from datetime import date, datetime

app = Flask(__name__)
#---------------------- prayTimes Object -----------------------


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


def map_prayerdata():
    timeNames = ['fajr', 'dhuhr', 'asr', 'maghrib', 'isha']
    new_iqama = ['+1', '+0', '+0', '+0', '+60']
    p_times = list(map(get_prayertime,timeNames))
    i_times = list(map(get_iqamatime, *(timeNames, new_iqama)))
    print("Prayer TImes =", p_times)
    print("Prayer TImes =", i_times)
    data = dict(zip(timeNames, list(zip(p_times,i_times))))
    print('Prayer Data = ',data)
    return data



@app.route("/")
def hello():

    print('Prayer Times for today in Eugene/Oregon\n' + ('=' * 41))
    data= map_prayerdata()
    # prayTimes.setMethod('ISNA')
    # times = prayTimes.getTimes(date.today(), (, ), -8, dst=1);
    # for i in ['Fajr', 'Sunrise', 'Dhuhr', 'Asr', 'Maghrib', 'Isha', 'Midnight']:
    #     print(i + ': ' + times[i.lower()])
    return render_template("index.html", data=data)

if __name__ == '__main__':
    map_prayerdata()
    app.run(debug=True)
