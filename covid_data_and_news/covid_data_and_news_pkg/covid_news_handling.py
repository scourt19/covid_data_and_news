'''Module that creates all the functionality for covid news'''
import json
import sched
import time
import requests

list_of_dictionaries = []
removed_items = []
title_list = []
s = sched.scheduler(time.time, time.sleep)

with open("config.json", "r", encoding="utf-8") as config_file:
    config = json.load(config_file)


def news_API_request(covid_terms = "Covid COVID-19 coronavirus") -> dict:
    '''
    Gather data from an api using an api key and return a dictionary of
    data that has been pulled from the api and saved to a json file called
    news_api_data.json.

    covid_terms (str): Keywords that are used to find data relating to
    a specific topic.
    json_data (dict): Ruturns a dictionary of items that have been pulled
    from the api.
    '''
    base_url = config["config_url"]
    query = covid_terms
    api_key = config["config_api_key"]
    complete_url = base_url + "q=" + query + "&apiKey=" + api_key
    response = requests.get(complete_url)
    json_data = response.json()
    with open('news_api_data.json', 'w', encoding="utf-8") as file:
        json.dump(json_data, file)
        file.close()
    return json_data

def parse_json_api_data(news_dict = 'news_api_data.json') -> list:
    '''
    Parse through the json data by opening the file and adding the titles
    and contents to their corresponding lists. Then return these lists.

    json_file (str): A json file that is written as a string.
    title_list (list): A list of titles that have been pulled from the api.
    content_list (list): A list of content that has been pulled from the api.
    '''
    with open(news_dict, 'r', encoding="utf-8") as file:
        data = json.load(file)
        articles = data["articles"]
        for article in articles:
            title = article["title"]
            content = article["content"]
            # This is used to see if there has been any more updates to the
            # news json file to add to the list and to make sure that there
            # are no articles getting added that have already been removed.
            if title not in title_list and title not in removed_items:
                list_of_dictionaries.append({
                    "title": title,
                    "content": content
                })
                title_list.append(title)
    file.close()
    return list_of_dictionaries


def update_news(title: str) -> list:
    '''
    Delete news if the title is in the argument unless the title is already
    in the removed_items list and if the title is in the list_of_dictionaries.
    This title is added to the list of dictionaries.

    title (str): A title that is used to see if the title in either removed_items list
    or if the list_of_dictionaries.
    removed_items (list): A list of titles that have been removed from the list of dictionaries.
    '''
    if title not in removed_items:
        for i in range(len(list_of_dictionaries)):
            if list_of_dictionaries[i]['title'] == title:
                removed_items.append(title)
                del list_of_dictionaries[i]
            else:
                continue
            break
    return removed_items


def schedule_news_updates(news_update_interval:int, news_update_name:str) -> None:
    '''
    Schedules updates to the covid news data at a given time interval
    by using the sched amd time modules.

    update_interval (int): An integer that uses time.time to pull the time
    and is required in the function to set the time in seconds for when the
    covid news data is to be updated.
    update_name (str): A string that is used to give a name to the update.
    '''
    s.enter(news_update_interval,1,news_API_request,())
    s.run()
    return f"{news_update_name} update has been completed"
