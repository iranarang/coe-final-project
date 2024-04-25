from jobs import get_job_by_id, update_job_status, store_job_result, q, rd
import json
import logging

# Used ChatGPT to fix errors, to fix test cases, format data, and error handling

logging.basicConfig(level=logging.DEBUG)

def load_data_from_redis():
    """
    Load data from Redis. This assumes the data is already loaded into Redis using the API.
    """
    data = rd.get('hgnc_data')
    if data:
        return json.loads(data)
    return None

@q.worker
def do_work(jobid):
    update_job_status(jobid, 'pending')


    job_info = get_job_by_id(jobid)    
    start_date_approved = job_info.get('start_date_approved')
    end_date_approved = job_info.get('end_date_approved')

    logging.debug(f"start date: {start_date_approved}")
    logging.debug(f"end date: {end_date_approved}")

    print("Processing job:", job_info)

    data = load_data_from_redis()

    locus_group_counts = {}
    logging.debug(f"locus_group_counts: {locus_group_counts}")


    for gene_data in data['response']['docs']:
        date_approved = gene_data.get('date_approved_reserved')
        if date_approved and start_date_approved <= date_approved <= end_date_approved:
            locus_group = gene_data.get('locus_group')
            if locus_group:
            # Increment count for locus_group or initialize to 1 if it doesn't exist
                locus_group_counts[locus_group] = locus_group_counts.get(locus_group, 0) + 1

    logging.debug(f"locus_group_counts: {locus_group_counts}")

    update_job_status(jobid, 'complete')
    store_job_result(jobid, locus_group_counts)




if __name__ == '__main__':
    do_work()