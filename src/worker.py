from jobs import get_job_by_id, update_job_status, q, rd, results
import json
import logging
import matplotlib.pyplot as plt
import io

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

        logging.debug(f"car_count_per_year: {car_count_per_year}")

        years = list(sorted(car_count_per_year.keys()))
        bev_counts = [car_count_per_year[year]['Battery Electric Vehicle (BEV)'] for year in years]
        phev_counts = [car_count_per_year[year]['Plug-in Hybrid Electric Vehicle (PHEV)'] for year in years]

        logging.debug(f"years: {years}")
        logging.debug(f"bev: {bev_counts}")
        logging.debug(f"phev: {phev_counts}")

        max_bev_count = max(bev_counts)
        min_phev_count = min(phev_counts)
        new_min_y = min_phev_count - 100
        new_max_y = max_bev_count + 100

        plt.plot(years, bev_counts, label='Battery Electric Vehicle (BEV)', color='blue')
        plt.plot(years, phev_counts, label='Plug-in Hybrid Electric Vehicle (PHEV)', color='green') 

        plt.xlim(start_year, end_year)
        plt.ylim(new_min_y, new_max_y)

        plt.xlabel('Year')
        plt.ylabel('Count')
        plt.title('Car Counts for BEV and PHEV per Year')
        plt.legend(['Battery Electric Vehicle', 'Plug-in-Hybrid Electric Vehicle'])
        plt.grid(True)
        plt.savefig('/plot.png')
        
        with open('/plot.png', 'rb') as f:
            img = f.read()

        results.hset(jobid, 'image', img)

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
