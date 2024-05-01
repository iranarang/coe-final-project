from jobs import get_job_by_id, update_job_status, store_job_result, q, rd
import json
import logging
import matplotlib.pyplot as plt

# Used ChatGPT to fix errors, to fix test cases, format data, and error handling

logging.basicConfig(level=logging.DEBUG)

def load_data_from_redis():
    """
    Load data from Redis. This assumes the data is already loaded into Redis using the API.
    """
    data = rd.get('ev_data')
    if data:
        return json.loads(data)
    return None

def perform_analysis(jobid):
    update_job_status(jobid, 'pending')

    job_info = get_job_by_id(jobid)    
    start_year = int(job_info.get('start_year'))
    end_year = int(job_info.get('end_year'))

    logging.debug(f"start year: {start_year}")
    logging.debug(f"end year: {end_year}")

    print("Processing job:", job_info)

    data = load_data_from_redis()

    if data:
        car_count_per_year = {}
        for entry in data['data']:
            year = int(entry[13])
            model = entry[16]
            if start_year <= year <= end_year:
                if year not in car_count_per_year:
                    car_count_per_year[year] = {'Battery Electric Vehicle (BEV)': 0, 'Plug-in Hybrid Electric Vehicle (PHEV)': 0}
                if model == "Battery Electric Vehicle (BEV)":
                    car_count_per_year[year]['Battery Electric Vehicle (BEV)'] += 1
                elif model == "Plug-in Hybrid Electric Vehicle (PHEV)":
                    car_count_per_year[year]['Plug-in Hybrid Electric Vehicle (PHEV)'] += 1
        
        ##update_job_status(jobid, 'complete')

        # Plotting
        years = list(sorted(car_count_per_year.keys()))
        logging.debug(f"years: {years}")
        bev_counts = [car_count_per_year[year]['Battery Electric Vehicle (BEV)'] for year in years]
        logging.debug(f"bev: {bev_counts}")

        phev_counts = [car_count_per_year[year]['Plug-in Hybrid Electric Vehicle (PHEV)'] for year in years]
        logging.debug(f"phev: {phev_counts}")

        plt.xticks(range(min(years), max(years)+1, 1))

        plt.plot(years, bev_counts, label='Battery Electric Vehicle (BEV)')
        plt.plot(years, phev_counts, label='Plug-in Hybrid Electric Vehicle (PHEV)')

        plt.xlabel('Year')
        plt.ylabel('Count')
        plt.title('Car Counts for BEV and PHEV per Year')
        plt.legend()
        plt.grid(True)
        plt.savefig('/app/plots/plot.png')
        plt.show()
        
        store_job_result(jobid, car_count_per_year)
        update_job_status(jobid, 'complete')
        
        print("Completed job:", job_info)

        logging.debug(f"Job {jobid} completed successfully.")
    else:
        update_job_status(jobid, 'failed')
        logging.debug(f"Job {jobid} failed due to missing data.")

@q.worker
def do_work(jobid):
    perform_analysis(jobid)


if __name__ == '__main__':
    do_work()
