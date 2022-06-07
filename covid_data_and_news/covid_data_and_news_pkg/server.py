'''Server running using flask for the covid data and news'''
import logging
import sched
import time
import json
from flask import Flask
from flask import render_template
from flask import request
from covid_data_handler import covid_API_request
from covid_data_handler import parse_json_covid_data
from covid_news_handling import news_API_request
from covid_news_handling import parse_json_api_data
from covid_news_handling import update_news


app = Flask(__name__)
covid_API_request()
covid_API_request("England","nation")
news_API_request()
s = sched.scheduler(time.time, time.sleep)
update = []
REPEAT_UPDATE_WORD = "Repeat update:True"
COVID_UPDATE_WORD = "Covid data update:True"
NEWS_UPDATE_WORD = "News update:True"
TIME_WORD = "Time:"
hospital_amount = parse_json_covid_data(covid_API_request("England", "nation"))[2]
total_deaths = parse_json_covid_data(covid_API_request("England", "nation"))[3]
news = parse_json_api_data()
with open("config.json", "r", encoding="utf-8") as config_file:
    config = json.load(config_file)

logging.basicConfig(filename=config["log_file"],level=logging.INFO, encoding="utf-8")

def add_scheduled_updates(title: str, contents:str) -> list:
    '''
    Adds updates to a list called update with the title and contents
    being represented in a dictionary in order for the html file too see
    what is the title and what is the contents.

    title (str): A string that has the name of the update and the scheduled
    time for the update.
    contents (str): A string that says whether the update should involve covid
    data or/and news data, and whether the update should be repeated.
    '''
    update.append({
        "title": title,
        "content": contents
    })


def delete_news_button(del_title: str) -> None:
    '''
    Deletes news off the dashboard if the the title of the news article
    is equal to the title of the argument.

    del_title (str): A string that is inputted for the title of the news
    article that is wanting to be deleted.
    '''
    for i in range(len(news)):
        if news[i]['title'] == del_title:
            del news[i]
            break


def delete_update_button(del_title: str) -> None:
    '''
    Deletes updates off the dashboard if the the title of the update
    is equal to the title of the argument.

    del_title (str): A string that is inputted for the title of the update
    that is wanting to be deleted.
    '''
    for i in range(len(update)):
        if update[i]['title'] == del_title:
            del update[i]
            break


def current_time_hhmm() -> str:
    '''
    A function that returns a string of the current time to be used when
    cheking if the update should occur.
    '''
    minutes= (time.gmtime().tm_min)
    # Corrects the minutes in order to have a 0 at the front if the
    # time is less then 10 minutes on the minute part of the clock.
    if minutes < 10:
        minutes = "0" + str(time.gmtime().tm_min)
    return str(time.gmtime().tm_hour) + ":" + str(minutes)



@app.route('/index')
def server():
    '''
    The server function that makes the website run.
    
    Every 60 seconds the page refreshes and it checks if the user has requested
    something such as adding an update or wanting to delete a news article.
    If the user has requested to do something then the website will immediatly refresh
    with what the user wanted to happen. The fucntionality of the website is that it can
    delete scheduled updates and news articles from the interface if the X button is pressed
    also you can schedule an update where every time the website refreshes it will check the
    time and if the time is equal to the one that has been set, it will update the data
    and delete the scheduled update if the repeat button was uncheked.
    '''
    s.run(blocking=False)
    text_field = request.args.get('two')
    repeat_update_box = request.args.get('repeat')
    covid_data_box = request.args.get('covid-data')
    news_box = request.args.get('news')
    delete_news = request.args.get('notif')
    delete_scheduled_update = request.args.get('update_item')
    if text_field:
        update_time = request.args.get('update')
        if repeat_update_box == 'repeat':
            repeat_update_bool = True
        else:
            repeat_update_bool = False
        if covid_data_box == 'covid-data':
            covid_data_bool = True
        else:
            covid_data_bool = False
        if news_box == 'news':
            news_bool = True
        else:
            news_bool = False
        if covid_data_bool or news_bool is True:
            schedule_update_title = f"Title:{text_field}, Time:{update_time}"
            schedule_update_content = f"Repeat update:{repeat_update_bool}, \
                Covid data update:{covid_data_bool}, News update:{news_bool}"
            add_scheduled_updates(schedule_update_title, schedule_update_content)
            logging.info(update_time, schedule_update_title, schedule_update_content)
        else:
            logging.warning('It is not possible to repeat an update that does not update anything')
    for i, item in enumerate(update):
        if current_time_hhmm() in item['title']:
            if COVID_UPDATE_WORD in item['content'] and NEWS_UPDATE_WORD in item['content'] \
                and REPEAT_UPDATE_WORD in item['content']:
                covid_API_request()
                covid_API_request("England","nation")
                news_API_request()
                logging.info('Covid and News data have been updated \
                    which will be repeated in 24 hours')
            elif COVID_UPDATE_WORD in item['content'] and NEWS_UPDATE_WORD not in \
                item['content'] and REPEAT_UPDATE_WORD in item['content']:
                covid_API_request()
                covid_API_request("England","nation")
                logging.info('Covid data has been updated which \
                    will be repeated in 24 hours')
            elif COVID_UPDATE_WORD not in item['content'] and NEWS_UPDATE_WORD in \
                item['content'] and REPEAT_UPDATE_WORD in item['content']:
                news_API_request()
                logging.info('News data has been updated which will be updates in 24 hours')
            elif COVID_UPDATE_WORD in item['content'] and NEWS_UPDATE_WORD in \
                item['content'] and REPEAT_UPDATE_WORD not in item['content']:
                covid_API_request()
                covid_API_request("England","nation")
                news_API_request()
                logging.info('Covid and News data have been updated')
                del update[i]
            elif COVID_UPDATE_WORD in item['content'] and NEWS_UPDATE_WORD not in \
                item['content'] and REPEAT_UPDATE_WORD not in item['content']:
                covid_API_request()
                covid_API_request("England","nation")
                logging.info('Covid data has been updated')
                del update[i]
            elif COVID_UPDATE_WORD not in item['content'] and NEWS_UPDATE_WORD in \
                item['content'] and REPEAT_UPDATE_WORD not in item['content']:
                news_API_request()
                logging.info('News data has been updated')
                del update[i]
    if delete_news:
        update_news(delete_news)
        logging.info('News article has been deleted')
    if delete_scheduled_update:
        delete_update_button(delete_scheduled_update)
        logging.info('Scheduled update has been deleted')
    return render_template(config["interface_template"],
        image = 'covid-mask.png',
        title = 'Daily Covid Update',
        location = parse_json_covid_data(covid_API_request())[0],
        local_7day_infections = parse_json_covid_data(covid_API_request())[1],
        nation_location = parse_json_covid_data(covid_API_request("England", "nation"))[0],
        national_7day_infections = parse_json_covid_data(covid_API_request("England", "nation"))[1],
        hospital_cases = f"Hospital cases: {hospital_amount}",
        deaths_total = f"Total deaths: {total_deaths}",
        news_articles = news,
        updates = update)



if __name__ == '__main__':
    app.run()
