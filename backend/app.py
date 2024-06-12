from flask import Flask, request, jsonify
import wbgapi as wb
import pandas as pd
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend access


@app.route("/wb", methods=["POST"])
@cross_origin()
def get_indicator():
    data = request.json  # Accessing the entire JSON data
    dataset = request.json["dataset"]
    country = request.json["country"]
    time_begin = request.json["time_begin"]
    time_end = request.json["time_end"]

    df = wb.data.DataFrame(dataset, country, range(
    int(time_begin), int(time_end)), index='time', numericTimeKeys=True, labels=True)  # Removed quotes around True
    df = pd.DataFrame(df)
    df = df.fillna(0)
    df = df.sort_values(by='Time', ascending=True)  # Corrected 'Time' to match your DataFrame column name
    core = df.to_dict()

    result_list = []
    for year, value in core[country].items():
        result_list.append({
            "year": year,
            "value": value
        })

    return jsonify(result_list)

@app.route("/wbseries")
@cross_origin()
def get_series_list():
    df = wb.series.list()
    df = pd.DataFrame(df)

    # Create the output dictionary
    data = {}

    # Iterate through each row of the DataFrame
    for index, row in df.iterrows():
        data[row['value']] = {'dataset': row['id'], 'name': row['value']}
    return jsonify(data)

@app.route("/wbcountry")
@cross_origin()
def get_countries_list():
    df = wb.economy.list()
    df = pd.DataFrame(df)

    # Create the output dictionary
    data = {}

    # Iterate through each row of the DataFrame
    for index, row in df.iterrows():
        data[row['value']] = {'dataset': row['id'], 'name': row['value']}
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)

