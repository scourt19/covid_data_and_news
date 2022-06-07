# Covid Data Handler

### Prerequisites

The version of python that was used to build this code was python 3.9.6. In order to use this code you must first pip3 install uk-covid19

### Installation

to install the code, use pip3 install covid_data_handler after this you will need to run server.py and type http://127.0.0.1:5000/index into your we brower in order to be able to see the data and interact with the interface.

### Getting Started

User input that is required in order for the code to be scheduled is for the user to:
- Add a time
- Add a title
- specify what updates will be done
- Specify if the update will be repeated

### Testing

The testing framework that should be used is pytest, if there are no errors, then thetesting will just follow through with no errors, however if there is an issue then an AssertionError will be returned

### Documentation

Both covid_data_handler and covid_news_handling modules are used heavily in the server.py file. When you first run the server file. Both the covid data and news is pulled by the api request function at the start of the code. The news that is created on the interface is the parse_json_api_data function that parses through the news api request. This creates a list of dictionaries in the right format to pop up on the screen. When a scheduled update has been submit, it gets added to the scheduled updates list which makes it pop up on the screen due to website refreshing. If there are any scheduled updates within the list when the page refreshes, it checks the time of the system and the time of the scheduled update to see if the time is the same. If the time is the same then it updates the relevant data. Then if the scheduled update is meant to be repeated, the update stays in the list, however if the update is not meant to be repeated then the update is deleted from the list, which removes it from the interface. If you want to remove a news article or a scheduled update then you can press on the X at the top right hand each of each box and the box with the information inside of it will be removed.

### Details

- Author: Stefan Court
- License: MIT License