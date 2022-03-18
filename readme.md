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
