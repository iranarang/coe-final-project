import json
import pytest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from jobs import _generate_jid, _instantiate_job, _save_job, add_job, get_job_by_id, update_job_status, store_job_result, jdb, results

# Used ChatGPT to fix errors, to fix test cases, format data, and error handling

def test_generate_jid():
    job_id = _generate_jid()
    assert isinstance(job_id, str)

def test__instantiate_job():
    jid = "test_id"
    status = "test_status"
    start_year = "2021"
    end_year = "2022"

    job = _instantiate_job(jid, status, start_year, end_year)

    assert job['id'] == jid
    assert job['status'] == status
    assert job['start_year'] == start_year
    assert job['end_year'] == end_year

def test_save_job():
    jid = "test_id"
    job_dict = {"id": jid, "status": "test_status", "start_year": "2020", "end_year": "2024"}

    _save_job(jid, job_dict)
    retrieved_job = json.loads(jdb.get(jid))

    assert retrieved_job == job_dict


def test_add_job():
    start_year = "2021"
    end_year = "2023"

    job = add_job(start_year, end_year)

    assert 'id' in job
    assert job['status'] == "submitted"
    assert job['start_year'] == start_year
    assert job['end_year'] == end_year


def test_get_job_by_id():
    start_year = "2018"
    end_year = "2020"

    job_dict = add_job(start_year, end_year)
    job_id = job_dict["id"]

    retrieved_job_data = get_job_by_id(job_id)

    assert retrieved_job_data["id"] == job_id
    assert retrieved_job_data["start_year"] == start_year
    assert retrieved_job_data["end_year"] == end_year


def test_update_job_status():
    start_year = "2020"
    end_year = "2022"

    job_dict = add_job(start_year, end_year)
    job_id = job_dict["id"]

    new_status = "completed"
    update_job_status(job_id, new_status)
    updated_job = get_job_by_id(job_id)

    assert updated_job["status"] == new_status

def test_store_job_result():
    jid = "test_id"
    car_count_per_year = {"TESLA": 10, "AUDI": 20}

    store_job_result(jid, car_count_per_year)
    stored_result = json.loads(results.get(jid))

    assert stored_result == car_count_per_year

if __name__ == '__main__':
    pytest.main()
