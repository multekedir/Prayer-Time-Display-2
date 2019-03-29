import praytimes as pt
import requests
import re
from datetime import date, datetime


#---------------------- prayTimes Object -----------------------
class Prayer:
    def __init__(url):

    timeNames = ['fajr', 'dhuhr', 'asr', 'maghrib', 'isha']
    self.new_iqama = ['+1', '+0', '+0', '+0', '+60']


    self.longitude= 44.049950
    self.latitude= -123.121024
    self.calculation= 'ISNA'
    self.daylight_savings= 1

    self.prayTimes = pt.PrayTimes(self.calculation);


    def get_prayertime(self, prayer):
            """
            get the time of Athan from the prayer_api.py file.
            Location is set to Eugene,OR. Can be changed by
            adjusting the long, lat and elevation.
            :param prayer: enter a prayer from one the list [fajr, sunrise, dhuhr, asr, maghrib, isha]
            :param format: adjust time format in '12h' or '24h'
            :return: Time of prayer
            """


            self.times = self.prayTimes.getTimes(date.today(), (self.longitude, self.latitude), -8, self.daylight_savings)

            return datetime.strptime(self.times[prayer], "%H:%M").strftime("%I:%M %p")

    def read_data(self, url):
        self.new_data = []
        print("Data file url =", url)
        r = requests.get(url, stream=True)
        for line in r.iter_lines():
            if line:
                self.new_data.append(str(line.decode('utf-8')).rstrip('\n'))
        return self.new_data

    def check_addition(self, input):
        if (len(input) == 2):
            return bool(re.match("\+[0-9]",input))
        else:
            return bool(re.match("\+([0-5])([0-9])",input))

    def check_phone(self, input):
        return bool(bool(re.fullmatch("1[0-2]|0[1-9]:[0-5][0-9] ?[AaPp][Mm]", input)))

    def validate(self, data):
        print("Valid check data =", data)
        self.result = []
        for i  in data:
            print("Valid check for =", i)
            if i.startswith('+'):
                self.result.append(check_addition(i))
            else:
                self.result.append(check_phone(i))
            print("Valid check =", self.result)
        return all(self.result) and len(self.result) == 5

    def save_data(self, func, names):
        if validate([func(i) for i in names]):
            self.myfile =  open("./static/iqama.txt", "w")
            for i in names:
                self.myfile.write(func(i)+'\n')

            self.myfile.close()
            return True
        else:
            return False



    def set_iqama(self, iqama, data_file):
        print("Data from file =", read_data(data_file))

        self.new_iqama=iqama

    def cal_iqama_time(self, hour, difference):

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
        self.hour, self.min = self.hour.strip('AM,PM, ').split(':')
        self.iqama_min = int(self.min) + difference
        # check if it is more than 59 min
        if self.iqama_min >= 60:
            self.iqama_min -= 60
            self.iqama_hour = int(self.hour) + 1

            if (len(str(self.iqama_min)) == 1):
                #make it to 00:00 format
                self.iqama_min = '0' + str(self.iqama_min)

            if (len(str(self.iqama_hour)) == 1):
                #make it to 00:00 format
                self.iqama_hour = '0' + str(self.iqama_hour)

            #check time change AM to PM and PM to AM
            if self.hour == '11':
                if period == "AM":
                    period = 'PM'
                elif period == 'PM':
                    period = 'AM'

            return str(self.iqama_hour) + ":" + str(self.iqama_min) + " "+ period
        return str(self.hour) + ":" + str(self.iqama_min) +  " "+period

    def get_iqamatime(self, prayer, datain):

        """
        Check id input is a static or an addition.
        user input can start with '+' or a static time '5:25 PM'
        calls prayer_api.py
        :return: static time ('4:30 PM') or adds the time from Athan api
        """

        self.time = get_prayertime(prayer)
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


    def map_prayerdata(self, url):
        self.new_iqama = read_data(url)
        self.p_times = list(map(get_prayertime,timeNames))
        self.i_times = list(map(get_iqamatime, *(timeNames, self.new_iqama)))
        print('*'*100)
        print("Prayer Times =", self.p_times)
        print("Prayer Times =", self.i_times)
        print("change =", self.new_iqama)
        self.data = dict(zip(timeNames, list(zip(self.p_times,self.i_times))))
        print('Prayer Data = ',self.data)
        print('*'*100)
        return self.data
