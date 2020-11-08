# Covid19 Alarm clock Backend

Flask backend powering covid19 alarm clock.

## Installation

1. This project uses [poetry](https://python-poetry.org/) to manage dependencies. Visit their website for installation instructions.
2. This project uses `make` for housekeeping. It should come preinstalled on most systems, but if it is not, then there are plenty tutorials online on how to install `make`.
3. `poetry install` to install all dependencies (including developement dependencies) required by this project.
4. Create a `config.json` in project root. It stores all API keys required by this backend. The shape of the config is described below.
5. `make start` starts a localhost server on port 5000.

## Configuration

All configuration of this project is stored in `./config.json`.  

You must obtain api keys from:
- NewsAPI
- OpenWeatherMap 

```json5
{
    "open_weather_api_key": "...", // api key of OpenWeatherMap
    "news_api_key": "..."          // api key of NewsAPI
}
```

## Project structure

### `./server`

The entry point for all code.

#### `./server/api`

Contains code for calling third-party APIs.

#### `./server/utils`

Contains general-purposed helper functions.

#### `./server/routes`

Contains code for handling different API endpoints of this server.
