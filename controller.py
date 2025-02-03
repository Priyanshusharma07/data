from flask import Flask, jsonify    # type: ignore
from Scraping_Service import Advance,StockTrade,FiftyTwoWeek,circuit
from redis_utils import read_from_redis

app = Flask(__name__)

@app.route('/advance', methods=['GET'])
def get_data():
    data = Advance()
    return jsonify(data)

@app.route('/fifty', methods=['GET'])
def get_fifty():
    fiftytwo = FiftyTwoWeek()
    return jsonify(fiftytwo)

@app.route('/stocktrade', methods=['GET'])
def get_stock():
    stocktrade = StockTrade()
    return jsonify(stocktrade)

@app.route('/circuit', methods=['GET'])
def get_circuit():
    Circuit = circuit()
    return jsonify(Circuit)



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
