import pytest
import requests

def test_submit_job_post():
    """Test the submit_job route."""
    data = {"start_year": 2010, "end_year": 2020}
    response = requests.post('http://127.0.0.1:5002/jobs', json=data)
    assert response.status_code == 200
    assert "Job added to queue" in response.text

def test_submit_job_get():
    response = requests.get('http://127.0.0.1:5002/jobs')
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_job():
    all_jobs_response = requests.get('http://127.0.0.1:5002/jobs')
    all_jobs = all_jobs_response.json()
    if all_jobs:
        job_id = all_jobs[0]["id"]
        response = requests.get('http://127.0.0.1:5000/jobs/'+job_id)
        assert response.status_code == 200
        assert isinstance(response.json(), dict)

def test_handle_data_post():
    """Test the POST request to handle_data route."""
    data = {"response": {"docs": [{"hgnc_id": "TEST_ID_1", "other_data": "test_data_1"}]}}
    response = requests.post('http://127.0.0.1:5002/data', json=data)
    assert response.status_code == 200

def test_handle_data_get():
    """Test the GET request to handle_data route."""
    response = requests.get('http://127.0.0.1:5002/data')
    assert response.status_code == 200

def test_handle_data_delete():
    """Test the DELETE request to handle_data route."""
    response = requests.delete('http://127.0.0.1:5002/data')
    assert response.status_code == 200
    assert "Data deleted from Redis" in response.text

def test_get_vin():
    """Test the GET request to the /vin route."""
    data = {"response": {"docs": [{"VIN": "123456789"}, {"VIN": "987654321"}]}}
    requests.post('http://127.0.0.1:5002/data', json=data)

    response = requests.get('http://127.0.0.1:5002/vin')
    assert response.status_code == 200  # Assuming data is available now

def test_get_car_by_vin():
    vin_number = "WAUTPBFF4H"
    response = requests.get(f'http://127.0.0.1:5002/vin/{vin_number}')
    assert response.status_code == 200  # Assuming the VIN number is found



