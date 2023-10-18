from app import app
from flask import Flask, request, jsonify,render_template,redirect
import sqlite3
import datetime


@app.route('/')
def index():
    return render_template('data_analysis.html')

@app.route('/upload_data', methods=['POST'])
def upload_data():
    try:
        data = request.get_json()  # get data posted as a json
        date = date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  
        distance_data = data['distance']
        status = data['status']
        waterLevel = data['waterlevel']
        print(date,distance_data,status,waterLevel)
        try:
            conn = sqlite3.connect('dataBaseOfDistance.db')
            conn.execute('INSERT INTO distance (date, distance_data,status,waterLevel) VALUES (?, ? ,? , ?)', (date, distance_data,status,waterLevel))
            conn.commit()

            conn.close()
            return jsonify({"message": "updata success!"}), 200
        except:
            return jsonify({"message": "updata failed!"}), 400
    except Exception as e:
        return jsonify({"error": "updata failed!", "message": str(e)}), 400

@app.route('/get_data', methods=['GET'])
def get_data():
    coon = sqlite3.connect('dataBaseOfDistance.db')
    c = coon.cursor()
    latest_data = c.execute("SELECT * FROM distance ORDER BY id DESC LIMIT 1").fetchone()
    distance = latest_data[2]
    status = latest_data[3]
    message = latest_data[3]
    waterLevel = latest_data[4]
    data_select = c.execute("SELECT * FROM distance ORDER BY id DESC LIMIT 50")
    date_ls = []
    distance_ls = []
    for one in data_select:
        date_ls.append(one[1])
        distance_ls.append(one[2])
    data_select = {'date':date_ls, 'distance':distance_ls}
    return_dict = {'data':data_select, 'status':status, 'message':message,'distance':distance,'waterLevel':waterLevel}
    return return_dict

    