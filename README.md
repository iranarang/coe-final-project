# The final dispatch
## Description
This project involves processing Electric Vehicle (EV) data and storing it in a Redis database through a Flask interface. It also includes job functionality for asynchronous data processing. The dataset offers extensive insights into various aspects of EV population demographics.
Here are some examples:
VIN: The unique identifier assigned to each Vehicle.
Model: The type of Vehicle model.
Model Year: The year the model was created.
Make: The type of Electric Vehicle.
There are many more that are found within the data as well.
## Included Files
1. `flask_api.py`
   This file reads includes four different functions:
    `submit_job`: This function handles POST and GET requests for creating new jobs and returning the existing jobs.
   `handle_data`: This function handles POST, GET, and DELETE requests for data loading into Redis, fetching data from Redis, and deleting all data in Redis.
   `all_genes`: This function returns a list of all gene IDs from Redis.
   `gene_id`: This function returns gene information for the given hgnc_id.
2. `worker.py`
    This file will contain all of the functionality needed to get jobs from the task queue and execute the jobs.
3. `jobs.py`
    This file will contain all functionality needed for working with jobs in the Redis database and the Hotqueue queue.
4. `Dockerfile`
    The Dockerfile is a recipe for creating a Docker image containing a sequential set of commands (a recipe) for installing and configuring the application.
5. `docker-compose.yaml`
    The docker compose simplifies the management of multi-container Docker applications using rules defined in a YAML file
6. `requirements.txt`
    The requirements file contains all the non-standard Python libraries essential for our application.
7. `test_flask_api.py`, `test_worker.py`, `test_jobs.py`
    These files contain the pytest unit tests for each respective file
8. `Makefile`
    This file automates the building and running process for docker.
9. `prod` directory

      app-prod-deployment-flask.yml

      app-prod-deployment-redis.yml

      app-prod-deployment-worker.yml

      app-prod-ingress-flask.yml

      app-prod-pvc-redis.yml

      app-prod-service-flask.yml

      app-prod-service-nodeport-flask.yml

      app-prod-service-redis.yml

    This directory contains the production files for Kubernetes.
10. `test`

       app-test-deployment-flask.yml

       app-test-deployment-redis.yml

       app-test-deployment-worker.yml

       app-test-ingress-flask.yml

       app-test-pvc-redis.yml

       app-test-service-flask.yml

       app-test-service-nodeport-flask.yml

       app-test-service-redis.yml
    This directory contains the testing files for Kubernetes.
11. `diagram.png`
    This file includes the software diagram for homework05.
## Building/Running Instructions
First, clone the repositiry to your local enviornment. Make sure you have git installed. You can type the following in the terminal:
`git clone git@github.com:iranarang/coe-final-project.git`
Make sure you have Docker, Flask, and Kubernetes installed.
```
pip install docker
pip install flask
sudo apt-get update && sudo apt-get install -y kubectl
```
### Deploying and testing the application on local hardware (e.g. Jetstream)
With all the tools in place, we can start building our app. Simply type:
	`make cycle`
This will handle everything from breaking down the Docker container to running our test files. If you prefer more control, you can run each step individually:
```
make down
make build
make up
make tests
make run-tests-inside-container	
```
### Deploying and testing the application on a Kubernetes cluster
To deploy the application on a Kubernetes cluster, follow these stages:

1. Apply Redis Configuration:
	Start by applying the Redis configuration, including PersistentVolumeClaim (PVC), Deployment, and Service.
	Navigate to the appropriate directory containing the Kubernetes configuration files for production or testing.
	Apply the configurations using the following commands:
	```
	cd kubernetes/prod
	kubectl apply -f app-prod-pvc-redis.yml
	kubectl apply -f app-prod-deployment-redis.yml
	kubectl apply -f app-prod-service-redis.yml
	
	cd kubernetes/test
	kubectl apply -f app-test-pvc-redis.yml
	kubectl apply -f app-test-deployment-redis.yml
	kubectl apply -f app-test-service-redis.yml
	```
2. Update Flask and Worker Configuration:

	After applying the Redis configurations, obtain the IP address of the Redis service.
	Update the Flask and Worker YAML files with the Redis service IP address. You can find this IP address by using the `kubectl get services` command and locating the entry for the Redis service.
	Navigate to the directory containing the Flask and Worker YAML files.
	Modify the YAML files (app-prod-deployment-flask.yml, app-test-deployment-flask.yml, app-prod-deployment-worker.yml, and app-test-deployment-worker.yml) to replace the placeholder <REDIS_SERVICE_IP> with the actual IP address of 	the Redis service.
4. Apply Flask and Worker Configurations:
   
	Once the YAML files are updated, apply the Flask and Worker configurations.
	Navigate to the appropriate directory (prod or test) containing the Kubernetes configuration files.
	Apply the configurations using the following commands:
	```
	cd kubernetes/prod
	kubectl apply -f app-prod-deployment-flask.yml
	kubectl apply -f app-prod-deployment-worker.yml

 	cd kubernetes/test
	kubectl apply -f app-test-deployment-flask.yml
	kubectl apply -f app-test-deployment-worker.yml
	```
6. Start Kubernetes Services:
   
	After applying all configurations, start the Kubernetes services.
	Navigate to the appropriate directory (prod or test) containing the Kubernetes configuration files.
	Apply the configurations using the following commands:
	```
	cd kubernetes/prod
	kubectl apply -f app-prod-service-flask.yml
	kubectl apply -f app-prod-service-nodeport-flask.yml

	cd kubernetes/test
	kubectl apply -f app-test-service-flask.yml
	kubectl apply -f app-test-service-nodeport-flask.yml
 	```

Once that's done, check to see if all the services are deployed:
`kubectl get services`
After deploying the test Pod, you can view the logs generated by the tests using the `kubectl logs <pod-name>` command. This command retrieves the logs from the specified Pod, allowing you to inspect the output of the test execution.
### Using the application on local hardware (e.g. Jetstream)
To run each route:
1. `curl -X POST localhost:5002/data`
    Posts data into Redis.
2. `curl localhost:5002/data`
    Returns all data from Redis.
3. `curl -X DELETE localhost:5002/data`
    Deletes all the data in Redis.
4. `curl localhost:5002/vin`
    Retrieves EV data from Redis and returns a list of VIN numbers.
5. `curl localhost:5002/vin/<vin_number>`
   Returns car data from Redis based on the provided VIN number.
6. `curl localhost:5002/jobs`
   Lists all existing job IDs
7. `curl localhost:5002/jobs -X POST -d '{"start_year": "<start_year>", "end_year": "<end_year>"}' -H "Content-Type: application/json"`
   Posts a job with the the start and end year. Make sure to use the parameters start and end year.
8. `curl localhost:5002/results/<job_id>`
   Returns the ‘Car Counts for BEV and PHEV per Year’ plot and car count per year for the specific job id from the worker file.

	To access this plot, you must access the volume mounted inside the worker Docker container. First, enter the following:
	
	`docker ps -a`
	
	It should return something like this:
	![Screenshot (138)](https://github.com/iranarang/coe-final-project/assets/143050090/c59c50b7-0e94-40b7-ab31-24777296739f)
	
	Then, copy the container ID of the worker container (in this case it would be 7e7d81805201). Now, enter:
	
	`docker exec -it <worker_id> /bin/bash`
	
	Then, enter with the path/to/location being where you want to save the file:
	
	`scp /app/plots/plot.png path/to/location`
	If you are logged into the student login server using ssh, you can enter:
	
	`scp /app/plots/plot.png <username>@student-login.tacc.utexas.edu:~/`
	
	Then, if the plot was scp onto a ssh server, on your local device, enter the following:
	
	`scp <username>@student-login.tacc.utexas.edu:~/plot.png ./` 
	
	If the plot was scp onto the local device with the first step, the second step is not needed. The plot should now be saved onto the local device and ready to be accessed. 


9. `curl localhost:5002/help`
   Lists all the routes within (all the routes previously shown)
### Using the application at a public endpoint
Now to run each route, you can type the `kubectl get services` again.
It should return this:
![Screenshot (136)](https://github.com/iranarang/coe-final-project/assets/143050090/0026014c-efb0-4836-8a86-edfc38966a3e)

Navigate to the PROD nodeport. Check what port it is mapped to. In this case, the port is mapped to 30123. Make sure to check if your port is something different and apply it accordingly.
To run each route:
1. `curl -X POST coe332.tacc.cloud:30123/data`
    Posts data into Redis.
2. `curl coe332.tacc.cloud:30123/data`
    Returns all data from Redis.
3. `curl -X DELETE coe332.tacc.cloud:30123/data`
    Deletes all the data in Redis.
4. `curl coe332.tacc.cloud:30123/vin`
    Retrieves EV data from Redis and returns a list of VIN numbers.
5. `curl coe332.tacc.cloud:30123/vin/<vin_number>`
   Returns car data from Redis based on the provided VIN number.
6. `curl coe332.tacc.cloud:30123/jobs`
   Lists all existing job IDs
7. `curl -X POST -d '{"start_year": "<start_year>", "end_year": "<end_year>"}' -H "Content-Type: application/json" coe332.tacc.cloud:30123/jobs`
   Posts a job with the the start and end year. Make sure to use the parameters start and end year.
8. `curl coe332.tacc.cloud:30123/results/<job_id>`
   Returns the ‘Car Counts for BEV and PHEV per Year’ plot and car count per year for the specific job id from the worker file.
9. `curl coe332.tacc.cloud:30123/help`
   Lists all the routes within (all the routes previously shown)
### Logging
To view logging messages, simply type  `docker ps -a` in the command line to get the container ID. Then, type `docker logs <container_id> in the command line to see the logging messages.
### Software Diagram
![software_diagram](https://github.com/iranarang/coe-final-project/assets/143050090/1679ca7a-380f-449d-8342-161b947953f2)

## Sample Code
```
@app.route('/vin', methods=['GET'])
def get_vin():
    vin_numbers = []
    if rd.exists('ev_data'):
        data = rd.get('ev_data')
        data_json = json.loads(data)
        for entry in data_json['data']:
            vin_numbers.append(entry[8])
    else:
        return "No data available in Redis", 404
    return jsonify(vin_numbers), 200
```
This function is from the `flask_api.py` file. Its purpose is to get the vin number from the electric vehicle data and returns a list of VIN numbers. It looks through the Redis database and checks if the data is there. If it is, it gets the vin number. If not, it returns an error message.
## Sample Results
If we were to curl the route `curl coe332.tacc.cloud:32308/vin`, the following output will return.
```
  "KNDC3DLC5N",
  "7SAYGDEE9P",
  "KM8KR4AE7P",
  "JTDKAMFP5M",
  "7SAYGDEF6P",
  "7SAYGAEE5P",
  "2C4RC1S75P",
  "YV4BR0DM8M",
  "KNDPZDAH7P",
  "1N4BZ0CP6G",
  "JTDKN3DPXD",
  "KM8KRDAF3P",
  "KNDPZDAH5P",
  "50EA1TEA7P",
  "1C4JJXP60N",
  "5YJ3E1EA0M",
  "5YJ3E1EC8L",
  "5YJSA1E27F"
```
This is a just a small section of the result. It shows the VIN numbers in a JSON format.


If we were the want to access the data for a specific VIN, we would curl the route `curl coe332.tacc.cloud:32308/vin/5YJSA1E27F`. The following output would occur,
```
 "2020 Census Tract": "53033032704",
  "Base MSRP": "0",
  "City": "North Bend",
  "Clean Alternative Fuel Vehicle (CAFV) Eligibility": "Clean Alternative Fuel Vehicle Eligible",
  "Congressional Districts": "8",
  "Counties": "3009",
```
This is a just a small section of the result. This gives the basic information associated with just this specific VIN number.


## Citations
Electric Vehicle data set: [https://www.genenames.org/download/archive/](https://catalog.data.gov/dataset/electric-vehicle-population-data)
