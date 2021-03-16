from flask import Flask, render_template, request, redirect, url_for, send_file, abort, send_file, send_from_directory, make_response
import os
import pandas as pd
from os.path import join, dirname, realpath
import mysql.connector
from pathlib import Path
from datetime import timedelta, date, datetime
import re
import csv
import json
import shutil

app = Flask("Assignment 2")

app.config["DEBUG"] = True
app.config['UPLOAD_FOLDER1'] = app.root_path + '/static/daily_reports'
app.config['UPLOAD_FOLDER2'] = app.root_path + '/static/time_series'
app.config['UPLOAD_FOLDER3'] = app.root_path + '/static/daily_reports_us'
app.config['UPLOAD_FOLDER4'] = app.root_path + '/static/query'
app.config['UPLOAD_FOLDER5'] = app.root_path
db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="Gary19990618",
    database="covid_data"
)
mycursor = db.cursor()

new_path = ""
real_path = ""
ALLOWED_FORMAT = set(['JSON', 'CSV', 'Text'])


def table_exists(cursor, table_name):
    sql = "show tables;"
    cursor.execute(sql)
    tables = [cursor.fetchall()]
    table_list = re.findall('(\'.*?\')', str(tables))
    table_list = [re.sub("'", '', each) for each in table_list]
    if table_name in table_list:
        return 1
    else:
        return 0


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
        table_name = os.path.splitext(file.filename)[0]
        table_name = table_name.replace('-', '_', 2)
        path = os.path.join(app.config['UPLOAD_FOLDER1'], table_name+'.csv')
        file.save(path)
        col_name = ['FIPS', 'Admin2', 'Province_State', 'Country_Region', 'Last_Update',
                    'Lat', 'Long_', 'Confirmed', 'Deaths', 'Recovered', 'Active', 'Combined_Key',
                    'Incidence_Rate', 'Case-Fatality_Ratio']
        csv_data = pd.read_csv(
            path, names=col_name, header=None, encoding='unicode_escape')  # modified
        csv_data = csv_data.where((pd.notnull(csv_data)), None)
        mycursor.execute("DROP TABLE IF EXISTS `{tab}`".format(tab=table_name))
        mycursor.execute("CREATE TABLE IF NOT EXISTS `{tab}` (FIPS VARCHAR(255), Admin2 VARCHAR(255), Province_State VARCHAR(255), Country_Region VARCHAR(255), Last_Update VARCHAR(255), Lat VARCHAR(255), Long_ VARCHAR(255), Confirmed VARCHAR(255), Deaths VARCHAR(255), Recovered VARCHAR(255), Active VARCHAR(255), Combined_Key VARCHAR(255), Incidence_Rate VARCHAR(255), `Case-Fatality_Ratio` VARCHAR(255))".format(tab=table_name))  # Add name without extension
        for i, row in csv_data.iterrows():
            sql = """INSERT INTO `{tab}` (FIPS, Admin2, Province_State, Country_Region, Last_Update, Lat, Long_, Confirmed, Deaths, Recovered, Active, Combined_Key, Incidence_Rate, `Case-Fatality_Ratio`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""".format(
                tab=table_name)  # Add name without extension
            val = (row['FIPS'], row['Admin2'], row['Province_State'], row['Country_Region'], row['Last_Update'], row['Lat'],
                   row['Long_'], row['Confirmed'], row['Deaths'], row['Recovered'], row['Active'], row['Combined_Key'],
                   row['Incidence_Rate'], row['Case-Fatality_Ratio'])
            mycursor.execute(sql, val)
            db.commit()
        return redirect(url_for('welcome_monitor'))
    return redirect(url_for('upload_daily_reports'))


@app.route('/monitor/daily_reports_us')
def daily_reports_us_index():
    return render_template('index_daily_reports_us.html')


@app.route('/monitor/daily_reports_us', methods=['POST'])
def upload_daily_reports_us():
    file = request.files['file']
    if file.filename != '':
        table_name = os.path.splitext(file.filename)[0]
        table_name = table_name.replace('-', '_', 2)
        path = os.path.join(
            app.config['UPLOAD_FOLDER3'], table_name + '_US.csv')
        file.save(path)
        col_name = ['Province_State', 'Country_Region', 'Last_Update', 'Lat', 'Long_', 'Confirmed', 'Deaths', 'Recovered', 'Active',
                    'FIPS', 'Incident_Rate', 'Total_Test_Results', 'People_Hospitalized', 'Case_Fatality_Ratio', 'UID', 'ISO3',
                    'Testing_Rate', 'Hospitalization_Rate']
        csv_data = pd.read_csv(path, names=col_name,
                               header=None, encoding='utf-8')
        csv_data = csv_data.where((pd.notnull(csv_data)), None)
        mycursor.execute("DROP TABLE IF EXISTS `{tab}`".format(
            tab=table_name + '_US'))
        mycursor.execute("CREATE TABLE IF NOT EXISTS `{tab}` (Province_State VARCHAR(255), Country_Region VARCHAR(255), Last_Update VARCHAR(255), \
                          Lat VARCHAR(255), Long_ VARCHAR(255), Confirmed VARCHAR(255), Deaths VARCHAR(255), Recovered VARCHAR(255), Active VARCHAR(255), \
                          FIPS VARCHAR(255), Incident_Rate VARCHAR(255), Total_Test_Results VARCHAR(255), People_Hospitalized VARCHAR(255), \
                          Case_Fatality_Ratio VARCHAR(255), UID VARCHAR(255), ISO3 VARCHAR(255), Testing_Rate VARCHAR(255), \
                          Hospitalization_Rate VARCHAR(255))".format(tab=table_name + '_US'))
        for i, row in csv_data.iterrows():
            sql = """INSERT INTO `{tab}` (Province_State, Country_Region, Last_Update, Lat, Long_, Confirmed, Deaths, Recovered, Active, FIPS, Incident_Rate, Total_Test_Results, People_Hospitalized, Case_Fatality_Ratio, UID, ISO3, Testing_Rate, Hospitalization_Rate) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""".format(tab=table_name + '_US')
            val = (row['Province_State'], row['Country_Region'], row['Last_Update'], row['Lat'], row['Long_'], row['Confirmed'],
                   row['Deaths'], row['Recovered'], row['Active'], row['FIPS'], row['Incident_Rate'], row['Total_Test_Results'],
                   row['People_Hospitalized'], row['Case_Fatality_Ratio'], row['UID'], row['ISO3'], row['Testing_Rate'],
                   row['Hospitalization_Rate'])
            mycursor.execute(sql, val)
            db.commit()
        return redirect(url_for('welcome_monitor'))
    return redirect(url_for('upload_daily_reports_us'))


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
        return redirect(url_for('welcome_monitor'))
    return redirect(url_for('upload_time_series'))


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
        for n in range(int((date2 - date1).days)+1):
            dt = date1 + timedelta(n)
            dates.append(dt.strftime("%m_%d_%Y"))
        if dates == []:
            # TODO: output!
            print("no dates")
        else:
            global real_path
            if detail['submit'] == "Search Countries and Download":
                countries = detail['countries'].split('/')
                country_data = {}
                for date in dates:
                    country_data[date] = {}
                    for country in countries:
                        sql_line = "SELECT Recovered FROM `{table}` WHERE Country_Region = (%s)".format(
                            table=date)
                        mycursor.execute(sql_line, (country,))
                        country_data[date][country] = mycursor.fetchall()
                country_file = open("country.txt", "w")
                str_country_data = repr(country_data)
                country_file.write("country_data = " + str_country_data + "\n")
                country_file.close()
                new_path = "country.txt"
                real_path = os.path.join(
                    app.config['UPLOAD_FOLDER5'], new_path)
                return redirect(url_for('download_file'))
            if detail['submit'] == "Search Provinces/States and Download":
                provinces = detail['provinces'].split('/')
                province_data = {}
                for date in dates:
                    province_data[date] = {}
                    for province in provinces:
                        sql_line = "SELECT Recovered FROM `{table}` WHERE Province_State = (%s)".format(
                            table=date)
                        mycursor.execute(sql_line, (province,))
                        province_data[date][province] = mycursor.fetchall()
                province_file = open("province.txt", "w")
                str_province_data = repr(province_data)
                province_file.write(
                    "provinces/states_data = " + str_province_data + "\n")
                province_file.close()
                new_path = "province.txt"
                real_path = os.path.join(
                    app.config['UPLOAD_FOLDER5'], new_path)
                return redirect(url_for('download_file'))
            if detail['submit'] == "Search Combined_keys and Download":
                combines = detail['combined_keys'].split('/')
                combine_data = {}
                for date in dates:
                    combine_data[date] = {}
                    for combine in combines:
                        sql_line = "SELECT Recovered FROM `{table}` WHERE Combined_Key = (%s)".format(
                            table=date)
                        mycursor.execute(sql_line, (combine,))
                        combine_data[date][combine] = mycursor.fetchall()
                combine_file = open("combined_keys.txt", "w")
                str_combine_data = repr(combine_data)
                combine_file.write("combined_key_data = " +
                                   str_combine_data + "\n")
                combine_file.close()
                new_path = "combined_keys.txt"
                real_path = os.path.join(
                    app.config['UPLOAD_FOLDER5'], new_path)
                return redirect(url_for('download_file'))

    return render_template('query.html')


@app.route('/monitor/query/download')
def download_file():
    return send_file(real_path, as_attachment=True)

@app.route('/monitor/<string:file_format>/<string:file_name>', methods=["GET"])
def data_returning_download(file_format, file_name):
    if not (file_format in ALLOWED_FORMAT):
        abort(404, description="no such format(we accept ['CSV', 'JSON', 'Text'])")
    if (file_name[0:11] != 'time_series' and table_exists(mycursor, file_name) != 1):
        abort(404, description="no such file, plase upload it first")
    if file_format == 'CSV':
        if (file_name[-2:] == 'US'):
            response = make_response(send_from_directory(app.config['UPLOAD_FOLDER3'], file_name + '.csv', as_attachment=True))
        elif (file_name[0:11] == 'time_series'):
            response = make_response(send_from_directory(app.config['UPLOAD_FOLDER2'], file_name + '.csv', as_attachment=True))
        else:
            response = make_response(send_from_directory(app.config['UPLOAD_FOLDER1'], file_name + '.csv', as_attachment=True))
        response.headers["Content-Disposition"] = "attachment; filename={}.csv".format(file_name)
        return response
    elif file_format == 'JSON':
        if (file_name[-2:] == 'US'):
            csv_file_path = os.path.join( app.config['UPLOAD_FOLDER3'], file_name + '.csv')
            json_file_path = os.path.join(app.config['UPLOAD_FOLDER3'], file_name + '.json')
            data = {}
            with open(csv_file_path) as csv_file:
                csv_reader = csv.DictReader(csv_file)
                for row in csv_reader:
                    id = row['Province_State']
                    data[id] = row
            with open(json_file_path, 'w') as json_file:
                json_file.write(json.dumps(data, indent=4))
            response = make_response(send_from_directory(app.config['UPLOAD_FOLDER3'], file_name + '.json', as_attachment=True))
        elif (file_name[0:11] == 'time_series'):
            csv_file_path = os.path.join(app.config['UPLOAD_FOLDER2'], file_name + '.csv')
            json_file_path = os.path.join(app.config['UPLOAD_FOLDER2'], file_name + '.json')
            data = {}
            with open(csv_file_path) as csv_file:
                csv_reader = csv.DictReader(csv_file)
                for row in csv_reader:
                    id = row['Province/State']
                    data[id] = row
            with open(json_file_path, 'w') as json_file:
                json_file.write(json.dumps(data, indent=4))
            response = make_response(send_from_directory(app.config['UPLOAD_FOLDER2'], file_name + '.json', as_attachment=True))
        else:
            csv_file_path = os.path.join(app.config['UPLOAD_FOLDER1'], file_name + '.csv')
            json_file_path = os.path.join(app.config['UPLOAD_FOLDER1'], file_name + '.json')
            data = {}
            with open(csv_file_path) as csv_file:
                csv_reader = csv.DictReader(csv_file)
                for row in csv_reader:
                    id = row['Province_State']
                    data[id] = row
            with open(json_file_path, 'w') as json_file:
                json_file.write(json.dumps(data, indent=4))
            response = make_response(send_from_directory(app.config['UPLOAD_FOLDER1'], file_name + '.json', as_attachment=True))
        response.headers["Content-Disposition"] = "attachment; filename={}.json".format(file_name)
        return response
    else:
        if (file_name[-2:] == 'US'):
            csv_file_path = os.path.join(app.config['UPLOAD_FOLDER3'], file_name + '.csv')
            txt_file_path = os.path.join(app.config['UPLOAD_FOLDER3'], file_name + '.txt')
            shutil.copy(csv_file_path, txt_file_path)
            response = make_response(send_from_directory(app.config['UPLOAD_FOLDER3'], file_name + '.txt', as_attachment=True))
        elif (file_name[0:11] == 'time_series'):
            csv_file_path = os.path.join(app.config['UPLOAD_FOLDER2'], file_name + '.csv')
            txt_file_path = os.path.join(app.config['UPLOAD_FOLDER2'], file_name + '.txt')
            shutil.copy(csv_file_path, txt_file_path)
            response = make_response(send_from_directory(app.config['UPLOAD_FOLDER2'], file_name + '.txt', as_attachment=True))
        else:
            csv_file_path = os.path.join(
                app.config['UPLOAD_FOLDER1'], file_name + '.csv')
            txt_file_path = os.path.join(
                app.config['UPLOAD_FOLDER1'], file_name + '.txt')
            shutil.copy(csv_file_path, txt_file_path)
            response = make_response(send_from_directory(app.config['UPLOAD_FOLDER1'], file_name + '.txt', as_attachment=True))
        response.headers["Content-Disposition"] = "attachment; filename={}.txt".format(file_name)
        return response
    return redirect(url_for('welcome_monitor'))


if __name__ == "__main__":
    app.run()
