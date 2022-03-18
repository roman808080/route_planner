from locust import HttpUser, task, constant


class Traveler(HttpUser):
    wait_time = constant(1)

    @task
    def plan_route(self):
        self.client.post("/route", json={"start": "a", "destination": "b", "strategy": "fastest"})
