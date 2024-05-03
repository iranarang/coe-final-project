import json
import os
import sys
import pytest
from unittest.mock import patch, mock_open
import logging
import tempfile
from pathlib import Path
import matplotlib as plt

logging.basicConfig(level=logging.DEBUG)

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from jobs import results, rd, q, add_job, get_job_by_id
from worker import do_work, perform_analysis

def test_perform_analysis():
    start_year = 2000
    end_year = 2030

    job_dict = add_job(start_year, end_year)
    logging.debug(f"job dict: {job_dict}")
    job_id = job_dict["id"]
    logging.debug(f"job id: {job_id}")
    assert(job_id)

    perform_analysis(job_id)

    job_info = get_job_by_id(job_id)
    logging.debug(f"job info: {job_info}")

    assert job_info['status'] == "complete"
