from flask import Flask, render_template, request, redirect, url_for
import os
import pandas as pd
from os.path import join, dirname, realpath
import mysql.connector


app = Flask("Assignment 2")

app.config["DEBUG"] = True
app.config['UPLOAD_FOLDER'] = 'static/daily_reports'

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database=""
)
mycursor = db.cursor()


@app.route('/monitor')
def welcome_monitor():
    return 'Welcome to the Covid Monitor!'


@app.route('/monitor/daily_reports')
def index():
    return render_template('index_daily_reports.html')


@app.route('/monitor/daily_reports', methods=['POST'])
def upload_daily_reports():
    file = request.files['file']
    if file.filename != '':
        path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(path)
        col_name = ['FIPS', 'Admin2', 'Province_State', 'Country_Region', 'Last_Update',
                    'Lat', 'Long_', 'Confirmed', 'Deaths', 'Recovered', 'Active', 'Combined_Key', 
                    'Incidence_Rate', 'Case-Fatality_Ratio']
        csv_data = pd.read_csv(path, names=col_name, header=None, encoding='utf-8')
        csv_data = csv_data.where((pd.notnull(csv_data)), None)
        mycursor.execute("CREATE TABLE IF NOT EXISTS `{tab}` (FIPS VARCHAR(255), Admin2 VARCHAR(255), Province_State VARCHAR(255), Country_Region VARCHAR(255), Last_Update VARCHAR(255), Lat VARCHAR(255), Long_ VARCHAR(255), Confirmed VARCHAR(255), Deaths VARCHAR(255), Recovered VARCHAR(255), Active VARCHAR(255), Combined_Key VARCHAR(255), Incidence_Rate VARCHAR(255), `Case-Fatality_Ratio` VARCHAR(255))".format(tab=file.filename))
        for i, row in csv_data.iterrows():
            sql = """INSERT INTO `{tab}` (FIPS, Admin2, Province_State, Country_Region, Last_Update, Lat, Long_, Confirmed, Deaths, Recovered, Active, Combined_Key, Incidence_Rate, `Case-Fatality_Ratio`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""".format(tab=file.filename)
            val = (row['FIPS'], row['Admin2'], row['Province_State'], row['Country_Region'], row['Last_Update'], row['Lat'],
                     row['Long_'], row['Confirmed'], row['Deaths'], row['Recovered'], row['Active'], row['Combined_Key'],
                     row['Incidence_Rate'], row['Case-Fatality_Ratio'])
            mycursor.execute(sql, val)
            db.commit()
    return redirect(url_for('welcome_monitor'))


if __name__ == "__main__":
    app.run()
