# Covid19 Alarm clock Backend

Flask backend powering covid19 alarm clock.

## Repo

[https://github.com/MrCreeper1008/covid19-alarm](https://github.com/MrCreeper1008/covid19-alarm)

## Author

Kenneth Ng (kenneth.ng.5226@outlook.com)

## Requirements

- Python >= 3.7

## Installation and getting started

1. Install the following packages:
    - Flask
    - python-dotenv
    - requests
    - uk-covid19
    - pyttsx3
    - pytest
2. Run `python -m flask run`
3. Server should be running locally at port 5000

### Troubleshooting

- `libespeak.so.1: cannot open shared object file: No such file or directory`
  - You're most likely using a Linux system. Install `espeak` and the error should go away. On Ubuntu/Ubuntu-like system: `sudo apt install espeak`.

## Configuration

All configuration of this project is stored in `./config.json`.

You must obtain api keys from:

- [NewsAPI](https://newsapi.org/register)
- [OpenWeatherMap](https://openweathermap.org/)

```json5
{
    // api key of OpenWeatherMap
    "open_weather_api_key": "...",

    // api key of NewsAPI
    "news_api_key": "...",

    // path to the templates folder, relative to ./server
    "templates_path": "...",

    // name of the main interface template in the templates folder
    "interface_template": "template.html",

    // path to the server log, including the file name.
    // "server.log" creates a log file called server.log in the root folder.
    "server_log_path": "...",
}
```

## Project structure

```tree
.
├── .flaskenv (stores Flask environment variables)
├── .pylintrc (pylint configuration)
├── .gitignore
├── Makefile
├── README.md
├── config.json (stores server configuration)
├── server (main entry to project code)
│   ├── __init__.py (server initialization code happens here)
│   ├── api (module that interacts with external apis)
│   │   ├── __init__.py
│   │   ├── covid.py   (interacts with uk-covid19)
│   │   ├── news.py    (interacts with newsapi.org)
│   │   └── weather.py (interacts with OpenWeatherAPI)
│   ├── routes (defines api endpoints of this server)
│   │   ├── __init__.py
│   │   └── alarms
│   │       ├── __init__.py
│   │       ├── alarm_scheduler.py (handles alarm scheduling)
│   │       ├── daily_brief.py     (generates daily brief messages)
│   │       ├── notification.py    (handles notifications)
│   │       └── route.py           (defines flask routes)
│   ├── static (stores static files)
│   │   └── images
│   │       └── logo.gif (logo of the website)
│   ├── templates
│   │   └── template.html (template of the main interface)
│   └── utils
│       └── logger.py (utilities for server logging)
└── server.log (logs of the server. can be configured in config.json)
```

Contains code for handling different API endpoints of this server.
