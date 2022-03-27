from locust import HttpUser, task, constant
import random


class Traveler(HttpUser):
    wait_time = constant(1)

    @task
    def plan_route(self):
        start_city_number = random.randrange(500)
        end_city_number = random.randrange(500)

        self.client.post("/route", json={"start": f"TestCity{start_city_number}",
                                         "destination": f"TestCity{end_city_number}", "strategy": "fastest"})
