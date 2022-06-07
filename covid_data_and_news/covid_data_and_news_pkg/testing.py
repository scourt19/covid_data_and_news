from covid_data_handler import parse_csv_data
from covid_data_handler import process_covid_csv_data
from covid_data_handler import covid_API_request
from covid_data_handler import parse_json_covid_data
from covid_data_handler import schedule_covid_updates
from covid_news_handling import news_API_request
from covid_news_handling import update_news
from covid_news_handling import parse_json_api_data
from covid_news_handling import schedule_news_updates
from server import add_scheduled_updates
from server import delete_news_button
from server import delete_update_button
from server import current_time_hhmm

def test_parse_csv_data_1():
    data = parse_csv_data('nation_2021-10-28.csv')
    assert len(data) == 639

def test_parse_csv_data_2():
    data = parse_csv_data('nation_2021-10-28.csv')
    assert isinstance(data, list)

def test_process_covid_csv_data():
    last7days_cases , current_hospital_cases , total_deaths = \
        process_covid_csv_data ( parse_csv_data (
            'nation_2021-10-28.csv' ) )
    assert last7days_cases == 240_299
    assert current_hospital_cases == 7_019
    assert total_deaths == 141_544

def test_covid_API_request():
    data = covid_API_request()
    assert isinstance(data, dict)

def test_schedule_covid_updates():
    schedule_covid_updates(update_interval=10, update_name='update test')

def test_news_API_request_1():
    assert news_API_request()
    assert news_API_request('Covid COVID-19 coronavirus') == news_API_request()

def test_news_API_requst_2():
    data = news_API_request()
    assert isinstance(data, dict)

def test_update_news():
    update_news('update title')

def test_schedule_news_updates():
    schedule_news_updates(news_update_inteval=10, news_update_name='update test')

def test_add_scheduled_updates():
    add_scheduled_updates('covid title', 'covid content')

def test_delete_news_button():
    delete_news_button('covid title')

def test_delete_update_button():
    delete_update_button('covid title')

def test_current_time_hhmm():
    current_time = current_time_hhmm()
    assert isinstance(current_time, str)

def test_parse_json_covid_data_1():
    location = parse_json_covid_data(covid_API_request())[0]
    local7_day_infection_rate = parse_json_covid_data(covid_API_request())[1]
    assert isinstance(location, str)
    assert isinstance(local7_day_infection_rate, int)

def test_parse_json_covid_data_2():
    location = parse_json_covid_data\
        (covid_API_request('England', 'nation'))[0]
    national7_day_infection_rate = parse_json_covid_data\
        (covid_API_request('England', 'nation'))[1]
    hospital_cases = parse_json_covid_data\
        (covid_API_request('England', 'nation'))[2]
    deaths_total = parse_json_covid_data\
        (covid_API_request('England', 'nation'))[3]
    assert isinstance(location, str)
    assert isinstance(national7_day_infection_rate, int)
    assert isinstance(hospital_cases, int)
    assert isinstance(deaths_total, int)

def test_parse_json_api_data():
    data = parse_json_api_data()
    assert isinstance(data, list)
