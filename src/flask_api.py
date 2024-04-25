from flask import Flask, request, jsonify
from jobs import add_job, get_job_by_id, rd, jdb, results
import redis
import requests
import json
from collections import OrderedDict

# Used ChatGPT to fix errors, to fix test cases, format data, and error handling

app = Flask(__name__)
rd = redis.Redis(host='redis-db', port=6379, db=0)

def load_data_into_redis():
    """
    This function obtains the data from the provided link and loads it into Redis.
    
    Returns:
        bool: True if the data was successfully loaded into Redis, False otherwise.
    """
    url = "https://data.wa.gov/api/views/f6w7-q2d2/rows.json?accessType=DOWNLOAD"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        rd.set('ev_data', json.dumps(data))
        return True
    else:
        return False

@app.route('/data', methods=['POST', 'GET', 'DELETE'])
def handle_data():
    """
    This function handles requests for data manipulation, including POST, GET, and DELETE methods.

    Returns:
        Depending on the request method:
        - For POST: Returns a success message if data is loaded into Redis successfully, otherwise returns a failure message.
        - For GET: Returns the data from Redis with a status code 200 if available, otherwise returns a message indicating no data available with status code 404.
        - For DELETE: Returns a message indicating data deletion from Redis with status code 200.
    """
    if request.method == 'POST':
        success = load_data_into_redis()
        if success:
            return "Data loaded into Redis successfully", 200
        else:
            return "Failed to load data into Redis", 500
    elif request.method == 'GET':
        data = rd.get('ev_data')
        if data:
            return data, 200, {'Content-Type': 'application/json'}
        else:
            return "No data available in Redis", 404
    elif request.method == 'DELETE':
        rd.delete('ev_data')
        return "Data deleted from Redis", 200
    
@app.route('/vin', methods=['GET'])
def get_vin():
    """
    Retrieves EV data from Redis and returns a list of VIN numbers.

    Returns:
        If data is available in Redis:
        - Returns a JSON array containing VIN numbers with status code 200.
        If no data is available in Redis:
        - Returns a message indicating no data available with status code 404.
    """
    vin_numbers = []
    if rd.exists('ev_data'):
        data = rd.get('ev_data')
        data_json = json.loads(data)
        for entry in data_json['data']:
            vin_numbers.append(entry[8])  
    else:
        return "No data available in Redis", 404
    
    return jsonify(vin_numbers), 200

@app.route('/vin/<vin_number>', methods=['GET'])
def get_car_by_vin(vin_number):
    """
    Retrieves car data from Redis based on the provided VIN number.

    Args:
        vin_number (str): The VIN number of the car to retrieve.

    Returns:
        If the car is found in Redis:
        - Returns a JSON representation of the car with status code 200.
        If the car is not found in Redis:
        - Returns a message indicating the car was not found with status code 404.
    """
    if rd.exists('ev_data'):
        data = rd.get('ev_data')
        data_json = json.loads(data)
        
        # Search for the provided VIN number in the dataset
        for entry in data_json['data']:
            if entry[8] == vin_number:
                # Create a dictionary to hold keys and values
                car_data = {}
                for index, key in enumerate(data_json['meta']['view']['columns']):
                    car_data[key['name']] = entry[index]
                return jsonify(car_data), 200
        
        # If VIN number not found, return 404
        return "Car with VIN number {} not found".format(vin_number), 404
    else:
        return "No data available in Redis", 404

@app.route('/jobs', methods=['GET', 'POST'])
def submit_job():
    """
    Handles job submissions and retrievals.

    Args:
        None

    Returns:
        - For POST: Returns a success message if job is successfully added to queue. Returns a failure message if not.
        - For GET: Returns the list of jobs if successful, otherwise returns a failure message.
    """

    if request.method == 'POST':
        data = request.get_json()
        if 'start_year' not in data or 'end_year' not in data:
            return "Invalid data provided. Both start_year and end_year are required.", 400
        start_year = data['start_year']
        end_year = data['end_year']
        add_job(start_year, end_year)
        return "Job added to queue.", 200
    elif request.method == 'GET':
        job_list = []
        for jid in jdb.keys():
            job_list.append(json.loads(jdb.get(jid)))
        return jsonify(job_list), 200
    else:
        return "Request not allowed", 405
    
@app.route('/jobs/<jobid>', methods=['GET'])
def get_job(jobid):
    """
    Retrieves job information associated with a job id.

    Args:
        jobid (str): The unique identifier of the job to retrieve information for.

    Returns:
        Returns the job information in JSON format if job id is found, otherwise returns a failure message.
    """
    return get_job_by_id(jobid)

@app.route('/results/<jobid>')
def get_job_result(jobid):
    
    result = results.get(jobid)
    if result is None:
        return "No results found for the provided job ID", 404
    else:
        return jsonify(json.loads(result)), 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)
