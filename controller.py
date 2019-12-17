import re
from datetime import date, datetime, timedelta

import json
import pytz

import praytimes as pt


# ---------------------- prayTimes Object -----------------------
class Prayer:
    """

    """

    def __init__(self):

        data = self.read_data()
        self.timeNames = ['fajr', 'dhuhr', 'asr', 'maghrib', 'isha']
        self.longitude = data['longitude']
        self.latitude = data['latitude']
        self.calculation = data['calculation']
        self.daylight_savings = data['dst']
        self.time_zone = data['time_zone']
        self.prayTimes = pt.PrayTimes(self.calculation)
        self.new_data_applied = True


    def __str__(self):

        return "longitude, %s. latitude %s. calculation %s. daylight_savings %s. time_zone %s." % (
            self.longitude, self.latitude, self.calculation, self.daylight_savings, self.time_zone)

    def __repr__(self):
        return "longitude, %s. latitude %s. calculation %s. daylight_savings %s. time_zone %s." % (
            self.longitude, self.latitude, self.calculation, self.daylight_savings, self.time_zone)

    @staticmethod
    def is_dst(zone_name):
        tz = pytz.timezone(zone_name)
        now = pytz.utc.localize(datetime.utcnow())
        return 1 if now.astimezone(tz).dst() != timedelta(0) is True else 0

    @staticmethod
    def read_data():
        with open('./static/data/data.json', 'r') as json_file:
            data = json.load(json_file)
        return dict(data)

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
        elif len(data) > 3:
            return False
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

    def change_setup(self, calculation, daylight_savings):
        """
        make changes to calculation method and daylight_savings
        :param calculation: str
        :param daylight_savings: int
        :return: None
        """
        self.daylight_savings = daylight_savings
        self.prayTimes = pt.PrayTimes(calculation)


    def get_prayertime(self, prayer):
        """
            get the time of Athan from the prayer_api.py file.
            Location is set to Eugene,OR. Can be changed by
            adjusting the long, lat and elevation.
            :param prayer: enter a prayer from one the list [fajr, sunrise, dhuhr, asr, maghrib, isha]
            :param format : adjust time format in '12h' or '24h'
            :return: Time of prayer
            """
        if self.new_data_applied is False:
            self.apply_new_data()
        times = self.prayTimes.getTimes(date.today(), (float(self.latitude), float(self.longitude)),
                                        timezone=self.time_zone, dst=self.is_dst('US/Pacific'), format='24h')
        return datetime.strptime(times[prayer], "%H:%M").strftime("%I:%M %p")

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

    def update_data(self, data, key):
        """
        collects the nessarey data from user and save the changes.

        :param func: data function
        :param names: prayer time names
        :param filename: name of file you want to change
        :param check: True if file need to be validated
        :return: True if file is saves
        """
        current = self.read_data()
        current[key] = data
        print(current)
        with open('./static/data/data.json', 'w') as outfile:
            json.dump(current, outfile)

        self.prayTimes = pt.PrayTimes(self.calculation)
        self.new_data_applied = False
        return True

    def get_new_iqama(self):
        """
        read from file and set the adjustment
        :param url: Path for iqama adjustment
        :return: None
        """
        return self.read_data()['iqama']

    @staticmethod
    def apply_difference(hour, difference):
        """
        Gets prayer time and split the string and add
        the min to the prayer time.
        If hour 11:50am and difference is 20 -> 12:10pm
        :param hour: 11:50 pm
        :param difference: 20
        :return: time in 12hr formats
        """
        # covert hour to datetime object
        date_time_obj = datetime.strptime(hour, '%I:%M %p')
        # add time change using timedelta
        return datetime.strftime((date_time_obj + timedelta(minutes=difference)), "%I:%M %p")

    def apply_new_data(self):
        data = self.read_data()
        self.longitude = data['longitude']
        self.latitude = data['latitude']
        self.calculation = data['calculation']
        self.daylight_savings = data['dst']
        self.time_zone = data['time_zone']

        self.new_data_applied = True

    def get_calculation_methods(self):
        """
        gets current prayer method
        :return: str
        """
        return [p for p in self.prayTimes.methods]

    def get_iqama_time(self, prayer, datain):
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
                return self.apply_difference(time, datain)

        elif ("pm" or "am" and ":" in datain) and (len(datain) > 6):
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

    def map_prayer_data(self):
        difference = self.get_new_iqama()
        p_times = list(map(self.get_prayertime, self.timeNames))
        i_times = list(
            map(self.get_iqama_time, *(self.timeNames, difference)))
        print('*' * 100)
        print(self)
        print("Prayer Times =", p_times)
        print("Iqama Times =", i_times)
        print("change =", difference)
        data = dict(zip(self.timeNames, list(zip(p_times, i_times))))
        print('Prayer Data = ', data)
        print('*' * 100)
        return data

    def get_difference(self) -> dict:
        """
        gets all the iqama changes
        :return: dict
        """
        return dict(zip(self.timeNames, self.get_new_iqama()))
