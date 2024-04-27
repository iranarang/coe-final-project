import json
import os
import sys
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from jobs import results, rd, q, add_job, get_job_by_id
from worker import perform_analysis

def test_perform_analysis():
    start_year = 2010
    end_year = 2020

    job_dict = add_job(start_year, end_year)
    job_id = job_dict["id"]

    perform_analysis(job_id)

    job_info = get_job_by_id(job_id)
    assert job_info['status'] == "complete"

if __name__ == "__main__":
    test_perform_analysis()

