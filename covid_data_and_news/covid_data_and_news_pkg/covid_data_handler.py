'''Module that creates all the functionality for covid data'''
import sched
import time
import json
from typing import Tuple
from typing import Union
from uk_covid19 import Cov19API

with open('config.json','r',encoding="utf-8") as config_file:
    config = json.load(config_file)
s = sched.scheduler(time.time, time.sleep)

def parse_csv_data(csv_filename: str) -> list:
    '''
    Open the csv file and return the file in a list format.

    csv_filename (str): The csv file written as a string.
    data (list): A list of strings from the csv file.
    '''
    data = open(csv_filename, 'r',encoding="utf-8").readlines()
    return data


def process_covid_csv_data(covid_csv_data:list) -> Tuple[int, int, int]:
    '''
    process the csv data by looping through a static file
    and returning three integers.

    covid_csv_data (list): The list of strings created by the function above.
    last7days_cases (int): Integer created by totalling up the
    last 7 days of covid cases from the last valid entry point of data.
    current_hospital_cases (int): Integer created by locating and returning
    the last valid entry point of data.
    total_deaths (int): Integer created by locating and returning the
    last valid entry point of data.
    '''
    new_list = []
    number = 0
    counter = 0
    for line1 in covid_csv_data:
        multiple_lists = line1.split(',')
        new_list.append(multiple_lists)
    new_list.pop(0)
    for index_no_data in range(len(new_list)):
        if new_list[index_no_data][6] == '\n':
            number += 1
        else:
            continue
    for index_1 in range(7):
        counter += eval(new_list[index_1+number+1][6])
    last7days_cases = counter
    for index_2 in range(len(new_list)):
        if new_list[index_2][5] == '':
            pass
        else:
            current_hospital_cases = eval(new_list[index_2][5])
            break
    for index_3 in range(len(new_list)):
        if new_list[index_3][4] == '':
            pass
        else:
            total_deaths = eval(new_list[index_3][4])
            break
    return last7days_cases, current_hospital_cases, total_deaths


def covid_API_request(location = "Exeter", location_type = "ltla") -> dict:
    '''
    Gather data from an api and return a dictionary of information
    from the api along with the location (local).

    location (str): String of location to be used when looking for the area name.
    location_type (str): String of location type to be used when looking for the area type.
    local_api_for_sched (dict): Dictionary of data pulled from the api, using the
    filters, local_area and local_cases. The data is then saved in a json file called
    local_covid19.json.
    location (str): String that is pulled from the argument to be used in the
    local location of the flask module.
    '''
    area_information= [
        f'areaType={location_type}',
        f'areaName={location}'
    ]

    cases_and_deaths = {
        "areaName":"areaName",
        "areaType":"areaType",
        "date":"date",
        "newCasesBySpecimenDate":"newCasesBySpecimenDate",
        "hospitalCases":"hospitalCases",
        "cumDailyNsoDeathsByDeathDate":"cumDailyNsoDeathsByDeathDate"
    }

    api = Cov19API(filters=area_information, structure=cases_and_deaths)
    api_as_json = api.get_json()
    if location_type ==  "ltla":
        with open(config["config_local_covid_data"], 'w',encoding="utf-8") as file:
            json.dump(api_as_json, file)
            file.close()
    elif location_type == "nation":
        with open(config["config_national_covid_data"], 'w',encoding="utf-8") as file:
            json.dump(api_as_json, file)
            file.close()
    return api_as_json

def parse_json_covid_data(api_json: dict) -> Union[Tuple[str, int], Tuple[str, int, int, int]]:
    '''
    Parse through the json data returning either 1 integer along
    with a location or 3 integers along with a location depending
    on what the location type is.

    api_json (dict): Dictionary of api data that has been created by the function
    covid_API_request.
    location (str): String that has been created by pulling the location name
    from the api.
    local_7day_infection_rate (int): Integer created by totalling up the
    last 7 days of local covid cases.
    national_7day_infection_rate: Integer created by totalling up the
    last 7 days of national covid cases.
    hospital_cases (int): Integer created by locating and returning
    the last valid entry point of data.
    deaths_total (int): Integer created by locating and returning the
    last valid entry point of data.
    '''
    counter = 0
    number = 0
    data = api_json['data']
    location = data[0]['areaName']
    location_type = data[0]['areaType']
    if location_type == "ltla":
        for index_no_data in range(len(data)):
            if data[index_no_data]['newCasesBySpecimenDate'] is None:
                number += 1
            else:
                continue
        for index_1 in range(7):
            # +1 is used because the first entry point of data is invalid
            local_number = data[index_1+1]['newCasesBySpecimenDate']
            counter += local_number
        local_7day_infection_rate = counter
        return location, local_7day_infection_rate
    elif location_type == "nation":
        for index_no_data in range(len(data)):
            if data[index_no_data]['newCasesBySpecimenDate'] is None:
                number += 1
            else:
                continue
        for index_1 in range(7):
            # +1 is used because the first entry point of data is invalid
            national_number = data[index_1+number+1]['newCasesBySpecimenDate']
            counter += national_number
        national_7day_infection_rate = counter
        for index_2 in range(len(data)):
            if data[index_2]['hospitalCases'] is None:
                pass
            else:
                hospital_cases = data[index_2]['hospitalCases']
                break
        for index_3 in range(len(data)):
            if data[index_3]['cumDailyNsoDeathsByDeathDate'] is None:
                pass
            else:
                deaths_total = data[index_3]['cumDailyNsoDeathsByDeathDate']
                break
    else:
        pass
    return location, national_7day_infection_rate, hospital_cases, deaths_total

def schedule_covid_updates(update_interval:int, update_name:str) -> None:
    '''
    Schedules updates to the covid data at a given time interval
    by using the sched amd time modules.

    update_interval (int): An integer that uses time.time to pull the time
    and is required in the function to set the time in seconds for when the
    covid data is to be updated.
    update_name (str): A string that is used to give a name to the update.
    '''
    s.enter(update_interval,1,covid_API_request,())
    s.enter(update_interval,1,covid_API_request,("England", "nation"))
    s.run()
    return f"{update_name} update has been complete"
