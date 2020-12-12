import pandas as pd
from datetime import datetime, date
from csv import reader
import json

months = ('january', 'february', 'march', 'april', 'may', 'june', 'july',
          'august', 'september', 'october', 'november', 'december')

months_short = ('jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul',

                'aug', 'sep', 'oct', 'nov', 'dec')
prayer_data = {}


def read_data():
    with open('./static/data/data.json', 'r') as json_file:
        global prayer_data
        prayer_data = json.load(json_file)


def save_json(data):
    with open('out.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def get_data_from_excel():
    """
    Reads excel data from file.

    Parameters:
        data (str): which prayer data athan or iqama

    Returns:
        DataFrame: prayer data
        Date      Fajr      Zuhr       Asr      Maghrib    Isha
        1         06:21:00  12:14:00  14:20:00  16:38:00  18:07:00
        2         06:21:00  12:15:00  14:21:00  16:39:00  18:08:00
        3         06:21:00  12:15:00  14:22:00  16:40:00  18:09:00
        4         06:21:00  12:16:00  14:22:00  16:41:00  18:10:00
    """
    file_name = f'prayer_data.xlsx'
    # print("Reading to excel ........")
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
    # print("Converting to csv ........")
    try:
        df = get_data_from_excel()
        for sheet_names in df.keys():
            file = f'{sheet_names.lower()}.csv'
            print(f'saving to {file}')
            df[sheet_names].to_csv(file)
        return True
    except:
        return False


def create_inner_json_structure(prayer_times):
    """
    Parameters:
        prayer_times(tuple) = ((Iqamah,Athan))

    Returns:
                Fajr: {
                    iqamah: string,
                    Athan: string,
                },
                sunrise: string,
                Zuhr: {
                    iqamah: string,
                    Attah: string,
                },
                Asr: {
                    iqamah: string,
                    Attah: string,
                },
                Maghrib: {
                    iqamah: string,
                    Attah: string,
                },
                Isha: {
                    iqamah: string,
                    Attah: string,
                },
    """
    prayer_with_times = \
        {
            "fajr": {
                "Iqamah": prayer_times[0][0],
                "Athan": prayer_times[0][1],
            },
            "sunrise": prayer_times[1][0],
            "zuhr": {
                "Iqamah": prayer_times[2][0],
                "Attah": prayer_times[2][1],
            },
            "asr": {
                "Iqamah": prayer_times[3][0],
                "Attah": prayer_times[3][1],
            },
            "maghrib": {
                "Iqamah": prayer_times[4][0],
                "Attah": prayer_times[4][1],
            },
            "isha": {
                "Iqamah": prayer_times[5][0],
                "Attah": prayer_times[5][1],
            }
        }
    return prayer_with_times


def get_athan_time(date):
    current_month = date.strftime("%b").lower()
    current_day = int(date.strftime("%d"))

    # check if data is loaded
    global prayer_data
    if not prayer_data:
        read_data()

    return prayer_data[current_month][current_day]

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
    for mon in months_short:
        file_name = f'{mon}.csv'

        with open(f'{mon}.csv', 'r') as data:

            csv_reader = list(reader(data))
            i = 0

            # print(f'Reading from {file_name} line number {len(csv_reader)}')
            obj = {}
            for i in range(2, len(csv_reader)):
                inner_structure = create_inner_json_structure([(csv_reader[i][3], csv_reader[i][2]),
                                                               (csv_reader[i][4]),
                                                               (csv_reader[i][6], csv_reader[i][5]),
                                                               (csv_reader[i][8], csv_reader[i][7]),
                                                               (csv_reader[i][10], csv_reader[i][9]),
                                                               (csv_reader[i][12], csv_reader[i][11])])

                number_date = int(csv_reader[i][0])
                # transform date from "1-Dec-20" to 1
                # number_date = int(datetime.strme(csv_reader[i][0], '%d-%b-%y').strftime("%d"))
                obj.update({number_date: inner_structure})
            to_json_month.update({mon: obj})

    save_json(to_json_month)
