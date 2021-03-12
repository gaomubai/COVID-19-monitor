from flask import Flask, render_template, request, redirect, url_for, send_file
import os
import pandas as pd
from os.path import join, dirname, realpath
import mysql.connector
from pathlib import Path
from datetime import timedelta, date, datetime

app = Flask("Assignment 2")

app.config["DEBUG"] = True
app.config['UPLOAD_FOLDER1'] = 'static/daily_reports'
app.config['UPLOAD_FOLDER2'] = 'static/time_series'
app.config['UPLOAD_FOLDER3'] = 'static/daily_reports_us'
app.config['UPLOAD_FOLDER4'] = 'static/query'
app.config['UPLOAD_FOLDER5'] = '/Users/leshiyang/Documents/2021winter/assignment-2-11-gaomubai-leshiyang/COVIDMonitor/'
db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database=""
)
mycursor = db.cursor()

new_path = ""
real_path = ""

@app.route('/monitor')
def welcome_monitor():
    return 'Welcome to the Covid Monitor!'


@app.route('/monitor/daily_reports')
def daily_reports_index():
    return render_template('index_daily_reports.html')


@app.route('/monitor/daily_reports', methods=['POST'])
def upload_daily_reports():
    file = request.files['file']
    if file.filename != '':
        path = os.path.join(app.config['UPLOAD_FOLDER1'], file.filename)
        file.save(path)
        col_name = ['FIPS', 'Admin2', 'Province_State', 'Country_Region', 'Last_Update',
                    'Lat', 'Long_', 'Confirmed', 'Deaths', 'Recovered', 'Active', 'Combined_Key', 
                    'Incidence_Rate', 'Case-Fatality_Ratio']
        csv_data = pd.read_csv(path, names=col_name, header=None, encoding='unicode_escape') #modified
        csv_data = csv_data.where((pd.notnull(csv_data)), None)
        table_name = os.path.splitext(file.filename)[0]
        table_name = table_name.replace('-', '_', 2)
        mycursor.execute("DROP TABLE IF EXISTS `{tab}`".format(tab=table_name))
        mycursor.execute("CREATE TABLE IF NOT EXISTS `{tab}` (FIPS VARCHAR(255), Admin2 VARCHAR(255), Province_State VARCHAR(255), Country_Region VARCHAR(255), Last_Update VARCHAR(255), Lat VARCHAR(255), Long_ VARCHAR(255), Confirmed VARCHAR(255), Deaths VARCHAR(255), Recovered VARCHAR(255), Active VARCHAR(255), Combined_Key VARCHAR(255), Incidence_Rate VARCHAR(255), `Case-Fatality_Ratio` VARCHAR(255))".format(tab=table_name))  #Add name without extension
        for i, row in csv_data.iterrows():
            sql = """INSERT INTO `{tab}` (FIPS, Admin2, Province_State, Country_Region, Last_Update, Lat, Long_, Confirmed, Deaths, Recovered, Active, Combined_Key, Incidence_Rate, `Case-Fatality_Ratio`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""".format(tab=table_name) #Add name without extension
            val = (row['FIPS'], row['Admin2'], row['Province_State'], row['Country_Region'], row['Last_Update'], row['Lat'],
                     row['Long_'], row['Confirmed'], row['Deaths'], row['Recovered'], row['Active'], row['Combined_Key'],
                     row['Incidence_Rate'], row['Case-Fatality_Ratio'])
            mycursor.execute(sql, val)
            db.commit()
    return redirect(url_for('welcome_monitor'))

@app.route('/monitor/daily_reports_us')
def daily_reports_us_index():
    return render_template('index_daily_reports_us.html')


@app.route('/monitor/daily_reports_us', methods=['POST'])
def upload_daily_reports_us():
    file = request.files['file']
    if file.filename != '':
        path = os.path.join(app.config['UPLOAD_FOLDER3'], file.filename)
        file.save(path)
        col_name = ['Province_State', 'Country_Region', 'Last_Update', 'Lat', 'Long_', 'Confirmed', 'Deaths', 'Recovered', 'Active', 
                    'FIPS', 'Incident_Rate', 'Total_Test_Results', 'People_Hospitalized', 'Case_Fatality_Ratio', 'UID', 'ISO3', 
                    'Testing_Rate', 'Hospitalization_Rate']
        csv_data = pd.read_csv(path, names=col_name, header=None, encoding='utf-8')
        csv_data = csv_data.where((pd.notnull(csv_data)), None)
        mycursor.execute("DROP TABLE IF EXISTS `{tab}`".format(tab=file.filename + '_US'))
        mycursor.execute("CREATE TABLE IF NOT EXISTS `{tab}` (Province_State VARCHAR(255), Country_Region VARCHAR(255), Last_Update VARCHAR(255), \
                          Lat VARCHAR(255), Long_ VARCHAR(255), Confirmed VARCHAR(255), Deaths VARCHAR(255), Recovered VARCHAR(255), Active VARCHAR(255), \
                          FIPS VARCHAR(255), Incident_Rate VARCHAR(255), Total_Test_Results VARCHAR(255), People_Hospitalized VARCHAR(255), \
                          Case_Fatality_Ratio VARCHAR(255), UID VARCHAR(255), ISO3 VARCHAR(255), Testing_Rate VARCHAR(255), \
                          Hospitalization_Rate VARCHAR(255))".format(tab=file.filename + '_US'))
        for i, row in csv_data.iterrows():
            sql = """INSERT INTO `{tab}` (Province_State, Country_Region, Last_Update, Lat, Long_, Confirmed, Deaths, Recovered, Active, FIPS, Incident_Rate, Total_Test_Results, People_Hospitalized, Case_Fatality_Ratio, UID, ISO3, Testing_Rate, Hospitalization_Rate) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""".format(tab=file.filename + '_US')
            val = (row['Province_State'], row['Country_Region'], row['Last_Update'], row['Lat'], row['Long_'], row['Confirmed'],
                     row['Deaths'], row['Recovered'], row['Active'], row['FIPS'], row['Incident_Rate'], row['Total_Test_Results'],
                     row['People_Hospitalized'], row['Case_Fatality_Ratio'], row['UID'], row['ISO3'], row['Testing_Rate'], 
                     row['Hospitalization_Rate'])
            mycursor.execute(sql, val)
            db.commit()
    return redirect(url_for('welcome_monitor'))

@app.route('/monitor/time_series')
def time_series_index():
    return render_template('index_time_series.html')

@app.route('/monitor/time_series', methods=['POST'])
def upload_time_series():
    file = request.files['file']
    if file.filename != '':
        path = os.path.join(app.config['UPLOAD_FOLDER2'], file.filename)
        my_file = Path(path)
        if my_file.is_file():
            os.remove(path)
        file.save(path)
        csv_data = pd.read_csv(path, names=None, header=0, encoding='unicode_escape')
        csv_data = csv_data.where((pd.notnull(csv_data)), None)
    return redirect(url_for('welcome_monitor'))


@app.route('/monitor/query')
def query_index():
    return render_template('query.html')

@app.route('/monitor/query', methods=['POST'])
def query_post():
    if request.method == "POST":
        detail = request.form
        dates = []
        date1 = datetime.strptime(detail["dates_from"], "%m_%d_%Y")
        date2 = datetime.strptime(detail["dates_to"], "%m_%d_%Y")
        for n in range(int ((date2 - date1).days)+1):
            dt = date1 + timedelta(n)
            dates.append(dt.strftime("%m_%d_%Y"))
        if dates == []:
            #TODO: output!
            print("no dates")
        else:
            global real_path
            if detail['submit'] == "Search Countries and Download":
                countries = detail['countries'].split('/')
                country_data = {}
                for date in dates:
                    country_data[date] = {}
                    for country in countries:
                        sql_line = "SELECT Recovered FROM `{table}` WHERE Country_Region = (%s)".format(table=date)
                        mycursor.execute(sql_line, (country,))
                        country_data[date][country] = mycursor.fetchall()
                country_file = open("country.txt", "w")
                str_country_data = repr(country_data)
                country_file.write("country_data = " + str_country_data + "\n")
                country_file.close()
                new_path = "country.txt"
                real_path = os.path.join(app.config['UPLOAD_FOLDER5'], new_path)
                return redirect(url_for('download_file'))
            if detail['submit'] == "Search Provinces/States and Download":
                provinces = detail['provinces'].split('/')
                province_data = {}
                for date in dates:
                    province_data[date] = {}
                    for province in provinces:
                        sql_line = "SELECT Recovered FROM `{table}` WHERE Province_State = (%s)".format(table=date)
                        mycursor.execute(sql_line, (province,))
                        province_data[date][province] = mycursor.fetchall()
                province_file = open("province.txt", "w")
                str_province_data = repr(province_data)
                province_file.write("provinces/states_data = " + str_province_data + "\n")
                province_file.close()
                new_path = "province.txt"
                real_path = os.path.join(app.config['UPLOAD_FOLDER5'], new_path)
                return redirect(url_for('download_file'))
            if detail['submit'] == "Search Combined_keys and Download":
                combines = detail['combined_keys'].split('/')
                combine_data = {}
                for date in dates:
                    combine_data[date] = {}
                    for combine in combines:
                        sql_line = "SELECT Recovered FROM `{table}` WHERE Combined_Key = (%s)".format(table=date)
                        mycursor.execute(sql_line, (combine,))
                        combine_data[date][combine] = mycursor.fetchall()
                combine_file = open("combined_keys.txt", "w")
                str_combine_data = repr(combine_data)
                combine_file.write("combined_key_data = " + str_combine_data + "\n")
                combine_file.close()
                new_path = "combined_keys.txt"
                real_path = os.path.join(app.config['UPLOAD_FOLDER5'], new_path)
                return redirect(url_for('download_file'))

    return render_template('query.html')

@app.route('/monitor/query/download')
def download_file():
    return send_file(real_path, as_attachment=True)


if __name__ == "__main__":
    app.run()
