
# Assignment 2 Starter Template

## Getting Started
 
 (You must have Python-3 and a package manager [pip] installed on your computer before you start)
 1. Install virtual environment in the assignment-2-11-gaomubai-leshiyang folder:
    * mac/linux: python3 -m venv venv
    * windows: py -3 -m venv venv

 2. Activate the virtual environment:
    * mac/linux: . venv/bin/activate
    * windows: venv\Scripts\activate

 3. install the dependencies in requirements.txt:
    * pip install -r requirements.txt

 4. Running COVIDMonitor:
    * cd COVIDMonitor
    * python main.py


  ### Deployment
  ```bash

https://covidmonitor-mubai-leshi-2.herokuapp.com

```
### Route
#### /monitor
Main page
#### /monitor/daily_reports
1) Upload daily_reports file, data stored locally and updata to database
2) If file already exists, it will update
#### /monitor/daily_reports_us
1) Upload daily_reports_US file, data stored locally and updata to database
2) If file already exists, it will update
#### /monitor/time_series
Upload time series file and data stored locally
#### /monitor/query/string:information
1) string in the route can be 'Deaths', 'Confirmed', 'Active', 'Recovered'
2) requested dates required in the format: mm_dd_yyyy
3) query by one or more countries, provinces/states, combined_key
4) press 'search' to download the requested data file
#### / monitor/data_returning/<string:file_format>/<string:file_name>
1) file_format can be 'CSV', 'JSON', 'Text'
2) file_name in the fomat: mm_dd_yyyy(daily report) or mm_dd_yyyy_US(US daily report ) or time_series_xxxxxx(Time series)
3) you need to up load file before you start download
4) if the file exists it will download automatically
## Running Tests

  

A starter template for unit tests can be found under tests/unit_tests.py

  

To run unit tests with coverage, run the following command in COVIDMonitor folder:

  

```bash

pytest --cov-report term --cov=COVIDMonitor ../tests/unit_tests.py

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
