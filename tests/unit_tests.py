from COVIDMonitor.main import app
import os
import unittest
import tempfile
import csv
import mysql.connector
from os import path

db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="Gary19990618",
    database="covid_data"
)
mycursor = db.cursor()


class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        app.testing = True

    def tearDown(self):
        pass

    def test_monitor(self):
        response = app.test_client().get('/monitor')

        assert response.status_code == 200
        assert response.data == b'Welcome to the Covid Monitor!'

    def test_upload_daily_report(self):
        with tempfile.NamedTemporaryFile('w+') as test_csv:
            writer = csv.writer(test_csv)
            writer.writerow(['FIPS', 'Admin2', 'Province_State', 'Country_Region', 'Last_Update', 'Lat', 'Long_',
                             'Confirmed', 'Deaths', 'Recovered', 'Active', 'Combined_Key', 'Incident_Rate', 'Case_Fatality_Ratio'])
            writer.writerow(['8051', 'Gunnison', 'Colorado', 'US', '2021-01-04 05:22:02', '38.66611652',
                             '-107.0320729', '725,6,0,719', '"Gunnison, Colorado, US"', '4151.872637727637', '0.8275862068965517'])
            test_data = dict(file=test_csv)
            response = app.test_client().post('/monitor/daily_reports',
                                              content_type='multipart/form-data', data=test_data, follow_redirects=True)
            assert response.status_code == 200
            result = [['FIPS', 'Admin2', 'Province_State', 'Country_Region', 'Last_Update', 'Lat', 'Long_', 'Confirmed', 'Deaths', 'Recovered', 'Active', 'Combined_Key', 'Incident_Rate', 'Case_Fatality_Ratio'], [
                '8051', 'Gunnison', 'Colorado', 'US', '2021-01-04 05:22:02', '38.66611652', '-107.0320729', '725,6,0,719', '"Gunnison, Colorado, US"', '4151.872637727637', '0.8275862068965517']]
            mycursor.execute("SELECT * FROM `{tab}`".format(tab=test_csv.name))
            myresult = mycursor.fetchall()
            i = 0
            for x in myresult:
                assert x == result[i]
                i = i + 1
            mycursor.execute(
                "DROP TABLE IF EXISTS `{tab}`".format(tab=test_csv.name))

    def test_upload_daily_report_US(self):
        with tempfile.NamedTemporaryFile('w+') as test_csv:
            writer = csv.writer(test_csv)
            writer.writerow(['Province_State', 'Country_Region', 'Last_Update', 'Lat', 'Long_', 'Confirmed', 'Deaths', 'Recovered', 'Active', 'FIPS',
                             'Incident_Rate', 'Total_Test_Results', 'People_Hospitalized', 'Case_Fatality_Ratio', 'UID', 'ISO3', 'Testing_Rate', 'Hospitalization_Rate'])
            writer.writerow(['Florida', 'US', '2021-01-02 05:30:44', '27.7663', '-81.6868', '1323315', '21673', '', '1301642.0',
                             '12.0', '6161.333477544677', '15703599.0', '', '1.6377808760574768', '84000012.0', 'USA', '73115.70581202293', ''])
            test_data = dict(file=test_csv)
            response = app.test_client().post('/monitor/daily_reports_us',
                                              content_type='multipart/form-data', data=test_data, follow_redirects=True)
            assert response.status_code == 200
            result = [['Province_State', 'Country_Region', 'Last_Update', 'Lat', 'Long_', 'Confirmed', 'Deaths', 'Recovered', 'Active', 'FIPS', 'Incident_Rate', 'Total_Test_Results', 'People_Hospitalized', 'Case_Fatality_Ratio', 'UID', 'ISO3', 'Testing_Rate',
                       'Hospitalization_Rate'], ['Florida', 'US', '2021-01-02 05:30:44', '27.7663', '-81.6868', '1323315', '21673', '', '1301642.0', '12.0', '6161.333477544677', '15703599.0', '', '1.6377808760574768', '84000012.0', 'USA', '73115.70581202293', '']]
            mycursor.execute(
                "SELECT * FROM `{tab}`".format(tab=test_csv.name + '_US'))
            myresult = mycursor.fetchall()
            i = 0
            for x in myresult:
                assert x == result[i]
                i = i + 1
            mycursor.execute("DROP TABLE IF EXISTS `{tab}`".format(
                tab=test_csv.name + '_US'))

    def test_upload_time_series(self):
        with tempfile.NamedTemporaryFile('w+') as test_csv:
            writer = csv.writer(test_csv)
            writer.writerow(['Province/State', 'Country/Region',
                             'Lat', 'Long', '1/22/20', '1/23/20', '1/24/20'])
            writer.writerow(['Territory', 'Australia',
                             '-35.4735', '149.0124', '12', '12', '12'])
            test_data = dict(file=test_csv)
            response = app.test_client().post('/monitor/time_series',
                                              content_type='multipart/form-data', data=test_data, follow_redirects=True)
            assert path.exists(test_csv.name) == True
            assert response.status_code == 200

    def test_upload_index(self):
        response = app.test_client().get('/monitor/time_series')
        assert b'Upload your Time Series' in response.data
        response = app.test_client().get('/monitor/daily_reports_us')
        assert b'Upload your US Daily Reports' in response.data
        response = app.test_client().get('/monitor/daily_reports')
        assert b'Upload your Daily Reports' in response.data

    def test_data_returning_index_csv_daily_report(self):
        response = app.test_client().get('/monitor/something/01_03_2021', content_type='multipart/form-data')
        assert response.status_code == 404
        assert b'no such format' in response.data
        response = app.test_client().get('/monitor/CSV/something', content_type='multipart/form-data')
        assert response.status_code == 404
        assert b'no such file' in response.data
        response = app.test_client().get('/monitor/Text/01_03_2021')
        assert response.content_length == 566720
        response = app.test_client().get('/monitor/CSV/01_03_2021')
        assert response.content_length == 566720
        response = app.test_client().get('/monitor/JSON/01_03_2021')
        assert response.content_length == 290441
        response = app.test_client().get('/monitor/Text/01_01_2021_US')
        assert response.content_length == 9502
        response = app.test_client().get('/monitor/CSV/01_01_2021_US')
        assert response.content_length == 9502
        response = app.test_client().get('/monitor/JSON/01_01_2021_US')
        assert response.content_length == 37386
        response = app.test_client().get('/monitor/Text/time_series_covid19_confirmed_global')
        assert response.content_length == 509008
        response = app.test_client().get('/monitor/CSV/time_series_covid19_confirmed_global')
        assert response.content_length == 509008
        response = app.test_client().get('/monitor/JSON/time_series_covid19_confirmed_global')
        assert response.content_length == 910900

    def test_query_index(self): 
        response = app.test_client().get('/monitor/query')
        assert b'Query data' in response.data

    def test_query(self):
        test_data = dict(dates_from = '01_03_2021', dates_to = '01_03_2021', countries = 'Afghanistan', submit = 'Search Countries and Download')
        response = app.test_client().post('/monitor/query', data=test_data, follow_redirects=True)
        assert response.content_length == 61
        test_data = dict(dates_from = '01_03_2021', dates_to = '01_03_2021', provinces = 'Fujian', submit = 'Search Provinces/States and Download')
        response = app.test_client().post('/monitor/query', data=test_data, follow_redirects=True)
        assert response.content_length == 63
        test_data = dict(dates_from = '01_03_2021', dates_to = '01_03_2021', combined_keys = 'Western Australia, Australia', submit = 'Search Combined_keys and Download')
        response = app.test_client().post('/monitor/query', data=test_data, follow_redirects=True)
        assert response.content_length == 81

