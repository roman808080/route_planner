# Route planner

## Assignment

Create a backend for mapping application for route planning between cities. It has to be asyncio web service with two major parts: administrators can via REST API add/remove/edit cities and roads between them and frontend-facing part for route planning. Each city has name and position (latitude and longitude). Each road between two cities has distance and average travel time properties. The content of /route  POST request has following structure:

```json
{
  "start": "Ostrava",
  "destination": "Brno",
  "strategy": "fastest" # or "shortest"
}
```

The example of response might be:

```json
{
  "distance_km": 168.43,
  "duration_minutes": 95,
  "route": ["Ostrava", "Bilovec", "Hranice", "Olomouc", "Prostejov", "Vyskov", "Brno"]
}
```

1. Solution should be dockerized, it should be easy to run just by typing docker-compose up in repository directory.
2. Create the web service with scalability in mind (it can handle more requests per second by up-scaling of the backend).
3. There is no need to implement any authorization of the administrator part of the API.
4. The storage of the data should be persistent. E.g. restarting of the solution does not erase the data.
5. Create a testing dataset of 500 cities and road network. It doesn't has to be real data.
6. Create a performance test that will run your solution, upload the test dataset and apply a load of 10 requests per second for 10 minutes. Create a small report afterwards. You can use stub for Locust (see `locust` directory and visit http://localhost:8089/).

### Questions:

1. How did you chose your persistent data storage? Were there another options for consideration?
2. What is the complexity of your route planner? How it will perform if there will be 10^6 citites and many routes between them?

### Optional but nice to have side-quests:

1. Add monitoring (e.g. Prometheus + Grafana). Measure errors, requests per second and requests durations
2. Add tracing (e.g. Jaeger)
3. Add frontend. Simple page with two input boxes (start, destination) and plan route button. Optionally you can visualize the planned route

## How to run the code

In order to run the code, you have to setup docker and docker-compose on your environment (https://docs.docker.com/get-docker/, https://docs.docker.com/compose/). Once you have this, use Make to run (`make up`) and test  (`make test`) the code.


## Locust report
The report is here -> https://github.com/roman808080/route_planner/blob/master/doc/test_report_for_locustfile.pdf

## Answers on questions above
1. I was trying to find something which can be easily dockerized and what can be used in production. For instance, it is relatively hard to dockerize Oracle Database. I can find only old versions of the database on dockerhub, and eventually I would need to build an Oracle linux container in which I would install the database (and it is not an open source project). I did not use SQLite because it cannot be used in production without troubles. I have not thought about using non-sql databases because I do not have much experince with them.

2. Time Complexity is O(E Log V) where, E is the number of cities and V is the number of roads.
   Space Complexity: O(V).
   It would perform poorly because I load all nodes to RAM, and it will eventually crash the process. I would need to optimize the algorithm to keep in memory only nodes which I really need. Also, the speed can be improved by using aioprocessing or a similar library which would allow to work on requests in background.

## Additional tasks
I have not done any of them, but I think I will touch them eventually.

UPDATE: I added prometheus without graphana. I have added some mesurements, but they are not sufficient. I plan to add a library (this one https://pythonawesome.com/prometheus-exporter-for-starlette-and-fastapi/ or this one https://pythonawesome.com/instrument-your-fastapi-app/) to speed up the development process. Otherwise I need to override default behaviour for capturing HTTPExceptions. After this I plant to add Grafana docker container and integrate it with prometheus (Of cource, I am not sure when it will be done).



## Additional notes (or minuses and disadvantages)

1. I have written tests with sqlite. The tests already pretty slow and will require optimization (~7 seconds on my machine). I think, at least fixtures should be optimized.
2. I commited .vscode files to the project to use it as an example in future.
3. I created 3 docker-compose files which should not be a case in the best of the worlds:
  - one I created to simplify debugging
  - another one for load tests
4. The load test can be further automated by using "-headless --reset-stats -t 30s --only-summary |& tee summary.txt" inside the load-test docker compose