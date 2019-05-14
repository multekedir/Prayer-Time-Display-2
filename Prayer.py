import praytimes as pt
import requests
import re
from datetime import date, datetime


# ---------------------- prayTimes Object -----------------------
class Prayer:
    """

    """

    def __init__(self):
        """

        """

        self.is_setup = False
        self.timeNames = ['fajr', 'dhuhr', 'asr', 'maghrib', 'isha']
        self.new_iqama = ['+0', '+0', '+0', '+0', '+0']

        self.longitude = 44.849401
        self.latitude = -123.240960
        self.calculation = 'ISNA'
        self.daylight_savings = 1
        self.time_zone = -8
        self.prayTimes = pt.PrayTimes(self.calculation)

        self.prayTimes.setMethod(self.calculation)

    def new_data(self, timeNames, longitude, latitude, calculation, time_zone,
                 new_iqama=['+0', '+0', '+0', '+0', '+0']):
        """

        :param timeNames:
        :param longitude:
        :param latitude:
        :param calculation:
        :param time_zone:
        :param new_iqama:
        """
        self.is_setup = False
        self.timeNames = timeNames
        self.new_iqama = new_iqama

        self.longitude = longitude
        self.latitude = latitude
        self.calculation = calculation
        self.daylight_savings = 1
        self.time_zone = time_zone

        self.prayTimes = pt.PrayTimes(self.calculation)
        self.prayTimes.setMethod(self.calculation)

    def setup(self, datafile, iqamafile):
        """
        apply the cahnges from file to iqama time
        :param datafile:
        :param iqamafile:
        :return:
        """
        self.is_setup = True
        self.change_setup(*(self.read_data(datafile)))
        self.set_iqama(iqamafile)

    def __str__(self):

        return "longitude, %s. latitude %s. calculation %s. daylight_savings %s. time_zone %s." % (
            self.longitude, self.latitude, self.calculation, self.daylight_savings, self.time_zone)

    def __repr__(self):
        return "longitude, %s. latitude %s. calculation %s. daylight_savings %s. time_zone %s." % (
            self.longitude, self.latitude, self.calculation, self.daylight_savings, self.time_zone)

    def __iter__(self):
        p_times = list(map(self.get_prayertime, self.timeNames))
        i_times = list(
            map(self.get_iqamatime, *(self.timeNames, self.new_iqama)))
        for prayer, iqama in (p_times, i_times):
            yield [prayer, iqama]

    def change_setup(self, calculation, daylight_savings):
        """
        make changes to calculation method and daylight_savings
        :param calculation: str
        :param daylight_savings: int
        :return: None
        """
        self.calculation = calculation
        self.daylight_savings = daylight_savings
        self.prayTimes.setMethod(calculation)

    def get_prayertime(self, prayer):
        """
            get the time of Athan from the prayer_api.py file.
            Location is set to Eugene,OR. Can be changed by
            adjusting the long, lat and elevation.
            :param prayer: enter a prayer from one the list [fajr, sunrise, dhuhr, asr, maghrib, isha]
            :param format: adjust time format in '12h' or '24h'
            :return: Time of prayer
            """

        times = self.prayTimes.getTimes(date.today(
        ), (self.longitude, self.latitude), self.time_zone, int(self.daylight_savings), '24')
        return datetime.strptime(times[prayer], "%H:%M").strftime("%I:%M %p")

    @staticmethod
    def read_data(url):
        """
        reads file data and store it in array
        :param url: file location
        :return: str
        """
        # print("Data file url =", url)
        new_data = []
        r = requests.get(url, stream=True)
        for line in r.iter_lines():
            if line:
                new_data.append(str(line.decode('utf-8')).rstrip('\n'))
        return new_data

    @staticmethod
    def write(func, names, filename):
        """
        gets data and save the data on to file.
        for each prayer load data and save on a newline
        :param func: function name
        :param names: prayer names
        :param filename: file to writ to
        :return: None
        """
        myfile = open(str("./static/" + filename), "w")
        # for each prayer load data and save on a newline
        for i in names:
            myfile.write(func(i) + '\n')

        myfile.close()

    @staticmethod
    def check_addition(data):
        """
        checks if data is between 0 and 59 with the addition sign
        :param data:
        :return:
        """
        if len(data) == 2:
            return bool(re.match("\+[0-9]", data))
        else:
            return bool(re.match("\+([0-5])([0-9])", data))

    @staticmethod
    def check_time(time):
        """
        Checks if the time entered has AM Or PM with no space after the time.
        Checks if the time entered has ':'
        Checks if the time entered has 4 digits
        :param time:
        :return:
        """
        return bool(bool(re.fullmatch("1[0-2]|0[1-9]:[0-5][0-9] ?[AaPp][Mm]", time)))

    def validate(self, data):
        """
        validate data based on what they start with. Return true if all match criteria.
        :calls check_addition and check_time
        :param data:
        :return: bool
        """
        # print("Valid check data =", data)
        # collection of chars
        result = []
        # for every letter
        for i in data:
            # print("Valid check for =", i)
            if i.startswith('+'):
                result.append(self.check_addition(i))
            else:
                result.append(self.check_time(i))
            # print("Valid check =", result)
        return all(result) and len(result) == 5

    def save_data(self, func, names, filename, check):
        """
        collects the nessarey data from user and save the changes.

        :param func: data function
        :param names: prayer time names
        :param filename: name of file you want to change
        :param check: True if file need to be validated
        :return: True if file is saves
        """
        if check:  # validation is needed
            if self.validate([func(i) for i in names]):
                self.write(func, names, filename)
                return True
        elif not check:
            self.write(func, names, filename)
            return True
        return False

    def set_iqama(self, url):
        """
        read from file and set the adjustment
        :param url: Path for iqama adjustment
        :return: None
        """
        # print("Iqama Data from file =", self.read_data(url))

        self.new_iqama = self.read_data(url)

    def cal_iqama_time(self, hour, difference):
        """
        Gets prayer time and split the string and add
        the min to the prayer time.
        If hour 11:50am and difference is 20 -> 12:10pm
        :param hour: 11:50pm
        :param difference: 20
        :return: time in 12hr formats
        """
        # '05:34 AM'
        period = hour[-2:]  # get the am and pm
        # get the time
        # hour = 05, min =34
        hour, min = hour.strip('AM,PM, ').split(':')
        iqama_min = int(min) + difference
        # check if it is more than 59 min
        if iqama_min >= 60:
            iqama_min -= 60
            iqama_hour = int(hour) + 1

            if len(str(iqama_min)) == 1:
                # make it to 00:00 format
                iqama_min = '0' + str(iqama_min)

            if len(str(iqama_hour)) == 1:
                # make it to 00:00 format
                iqama_hour = '0' + str(iqama_hour)

            # check time change AM to PM and PM to AM
            if hour == '11':
                if period == "AM":
                    period = 'PM'
                elif period == 'PM':
                    period = 'AM'

            return str(iqama_hour) + ":" + str(iqama_min) + " " + period
        return str(hour) + ":" + str(iqama_min) + " " + period

    def get_claculation_methods(self):
        """
        gets curent prayer method
        :return: str
        """
        return [p for p in self.prayTimes.methods]

    def get_iqamatime(self, prayer, datain):
        """
        Check id input is a static or an addition.
        user input can start with '+' or a static time '5:25 PM'
        calls prayer_api.py
        :return: static time ('4:30 PM') or adds the time from Athan api
        """

        time = self.get_prayertime(prayer)
        if datain.startswith('+'):
            datain.strip('+')
            try:
                datain = int(datain)
            except ValueError:
                print("Oops!  That was no valid number.  Try again...")
            else:
                iqama = self.cal_iqama_time(time, datain)
                return iqama
        elif (("pm" or "am" and ":" in datain) and (len(datain) > 6)):
            return datain
        return "ERROR"

    def get_info(self):
        print('*' * 100)
        print("Prayer longitude =", self.longitude)
        print("Prayer latitude =", self.latitude)
        print("Prayer calculation =", self.prayTimes.getMethod())
        print("Prayer dst =", self.daylight_savings)
        print("Prayer zone =", self.time_zone)
        print('*' * 100)

    def map_prayerdata(self):
        p_times = list(map(self.get_prayertime, self.timeNames))
        i_times = list(
            map(self.get_iqamatime, *(self.timeNames, self.new_iqama)))
        print('*' * 100)
        print(self)
        print("Prayer Times =", p_times)
        print("Iqama Times =", i_times)
        print("change =", self.new_iqama)
        data = dict(zip(self.timeNames, list(zip(p_times, i_times))))
        print('Prayer Data = ', data)
        print('*' * 100)
        return data

    def get_difference(self) -> dict:
        """
        gets all the iqama changes
        :return: dict
        """
        return dict(zip(self.timeNames, self.new_iqama))
