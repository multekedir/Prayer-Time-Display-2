import json
from csv import reader
from datetime import datetime

import pandas as pd

months = ('january', 'february', 'march', 'april', 'may', 'june', 'july',
          'august', 'september', 'october', 'november', 'december')

months_short = ('jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul',
                'aug', 'sep', 'oct', 'nov', 'dec')
prayer_data = {}

FOLDER_NAME = 'temp'


def read_data():
    """
    reads the data from our json file named out.json and
    """
    global prayer_data
    try:
        with open(f'{FOLDER_NAME}/out.json', 'r') as json_file:
            prayer_data = json.load(json_file)
    except FileNotFoundError:
        build_json()
        with open(f'{FOLDER_NAME}/out.json', 'r') as json_file:
            prayer_data = json.load(json_file)
    finally:
        return True
    return False


def save_json(data):
    """
    Parameters:
        data (dict) : the data from all csv files
    """
    with open(f'{FOLDER_NAME}/out.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def get_data_from_excel():
    """
    Reads excel data from file.

    Returns:
        DataFrame: prayer data
        Date      Fajr      Zuhr       Asr      Maghrib    Isha
        1         06:21:00  12:14:00  14:20:00  16:38:00  18:07:00
        2         06:21:00  12:15:00  14:21:00  16:39:00  18:08:00
        3         06:21:00  12:15:00  14:22:00  16:40:00  18:09:00
        4         06:21:00  12:16:00  14:22:00  16:41:00  18:10:00
    """
    file_name = f'./static/data/prayer_data.xlsx'
    print("Reading to excel ........")
    if check_data_from_file(file_name):
        return pd.read_excel(file_name, sheet_name=None)
    return None


def check_data_from_file(file_name):
    """
    Returns:
        bool: True if the excel sheet has all the month
    """
    # print("checking data ........")
    xl = pd.ExcelFile(file_name)
    return all(ele.lower() in months_short for ele in xl.sheet_names)


def convert_excel_sheets_to_csv():
    """
    reads multiple excel sheets and covert them to csv files

     Returns:
         true: if secsful
    """
    print("Converting to csv ........")
    try:
        df = get_data_from_excel()
        for sheet_names in df.keys():
            file = f'{FOLDER_NAME}/{sheet_names.lower()}.csv'
            print(f'saving to {file}')
            df[sheet_names].to_csv(file)
        return True
    except:
        return False


def get_athan_time(date):
    current_month = date.strftime("%b").lower()
    current_day = date.strftime("%d").lstrip('0')

    # check if data is loaded
    global prayer_data
    if not prayer_data:
        print("Getting new reading from file")
        if not read_data():
            return None
    try:
        out = prayer_data[current_month][current_day]
        print(f"Current Month {current_month} Day: {current_day}")
        print(f"Current Month data {prayer_data[current_month]}")
    except KeyError:
        print("ERROR while parsing the file. Please look at the template")
        return None

    return out


def create_inner_structure(pt_list):
    """
    Get's a row form the csv file and then build a list for athan and iqamah from the file.

   Parameters:
       pt_list(list): a row from the csv file

    Returns:
         {"fajr": (row[0], row[1]),
           "sunrise": (row[2]),
           "dhuhr": (row[3], row[4]),
           "asr": (row[5], row[6]),
           "maghrib": (row[7], row[8]),
           "isha": (row[9], row[10])}

    """
    # print(f'creating inner structure from list: {pt_list}')
    row = [datetime.strptime(pt_list[j], "%H:%M:%S").strftime("%I:%M %p") for j in range(3, len(pt_list))]
    # print(f'Time is now converted {pt_list}')
    pt_names = ["fajr", "sunrise", "dhuhr", "asr", "maghrib", "isha"]

    return {pt_names[i]: (row[i], row[i + 1]) for i in range(len(pt_names))}


def build_json():
    """
    Returns (dict):
        {
        month: {
             date: {
               inner_structure
            }
        }
    }
    """
    to_json_month = {}
    convert_excel_sheets_to_csv()
    # open all the csv files
    for mon in months_short:
        with open(f'{FOLDER_NAME}/{mon}.csv', 'r') as csvfile:
            csv_reader = list(reader(csvfile))
            obj = {}

            # jump the first two headers
            for i in range(2, len(csv_reader)):
                # csv_reader[i] a row from the CSV
                inner_structure = create_inner_structure(csv_reader[i])
                number_date = int(csv_reader[i][0])
                # transform date from "1-Dec-20" to 1
                # number_date = int(datetime.strme(csv_reader[i][0], '%d-%b-%y').strftime("%d"))
                obj.update({number_date: inner_structure})
            to_json_month.update({mon: obj})

    save_json(to_json_month)

    return to_json_month
