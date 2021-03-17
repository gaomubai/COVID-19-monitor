
# Assignment 2 Starter Template

  

## Getting Started

  

These instructions will get a copy of the assignment starter template up and running on your local machine.

  

### Prerequisites

  

You must have Python-3 and a package manager [pip] installed on your computer

  

Additionally you will need to install the following packages:

  

```bash

pip install flask

pip install pytest

pip install pytest-cov

```

  

### Running The Code

  

You can start by running main.py, which is in the folder COVIDMonitor. main.py has the main method that will start the program.

  
  

```bash

python main.py

```

  ### Deployment
  ```bash

https://covidmonitor-mubai-leshi-2.herokuapp.com

```
### Route
#### /monitor
Main page
#### /monitor/daily_reports
TODO
#### /monitor/daily_reports_us
TODO
#### /monitor/time_series
Upload time series file and data stored locally
#### /monitor/query/string:information
1) string in the route can be 'Deaths', 'Confirmed', 'Active', 'Recovered'
2) requested dates required in the format: mm_dd_yyyy
3) query by one or more countries, provinces/states, combined_key
4) press 'search' to download the requested data file
## Running Tests

  

A starter template for unit tests can be found under tests/unit_tests.py

  

To run unit tests with coverage, run the following command:

  

```bash

pytest --cov-report term --cov=COVIDMonitor tests/unit_tests.py

```

  

## Assignment Instructions

  

Assignment instructions can be found here: https://drive.google.com/file/d/1CX_c29slK1TyUvEOiolSzuugnRGCRp8A/view?usp=sharing

  

## Pair Programming

  

1. Add a new data file:

* Time Series: Driver:Leshiyang Navigator: Gaomubai

* Daily reports: Driver:Gaomubai Navigator: Leshiyang

2. Update existing files: Driver:Gaomubai Navigator: Leshiyang

3. Query data: Driver:Leshiyang Navigator: Gaomubai

4. Returning the data: Driver:Gaomubai Navigator: Leshiyang