# coe-final-project

curl -X POST http://localhost:5002/data
curl http://localhost:5002/data
curl -X DELETE http://localhost:5002/data
curl http://localhost:5002/vin
curl http://localhost:5002/vin/5YJSA1E27F
curl localhost:5002/jobs
curl localhost:5002/jobs -X POST -d '{"start_year": "2003", "end_year": "2007"}' -H "Content-Type: application/json"
curl localhost:5002/results