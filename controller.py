from flask import Flask, jsonify    # type: ignore
from advance import scrape_nse_data
from FiftyTwoEquity import FiftyTwoWeek
from circuit import circuit
from stocktrade import Stock
from redis_utils import read_from_redis

app = Flask(__name__)

@app.route('/advance', methods=['GET'])
def get_data():
    data = scrape_nse_data()
    return jsonify(data)

@app.route('/fifty', methods=['GET'])
def get_fifty():
    fifty = FiftyTwoWeek()
    return jsonify(fifty)

@app.route('/stocktrade', methods=['GET'])
def get_stock():
    trade = Stock()
    return jsonify(trade)

@app.route('/circuit', methods=['GET'])
def get_circuit():
    Circuit = circuit()
    return jsonify(Circuit)


# @app.route('/data', methods=['GET'])
# def getdata():
#    return  read_from_redis("api_response:http://127.0.0.1:5000/circuit")


api_keys = [
    "advance",
    "fifty",
    "stocktrade",
    "circuit"
]



@app.route('/fetch_data', methods=['GET'])  # Renamed the route to /fetch_data
def fetch_data():  # Renamed the function to avoid conflict
    data = []
    
    # Hit each Redis key one by one
    for api_key in api_keys:
        response_data = read_from_redis(api_key)
        data.append(response_data)  # Store the response in the dictionary
    
    return jsonify(data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
