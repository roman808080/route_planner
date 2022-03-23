from models import City, CityResponse, Road, RoadResponse


def add_city_to_db(client, name):
    response = client.post("/city", json=City(name=name,
                                              lattitude=0, longitude=0).dict())
    city_response = CityResponse(**response.json())
    assert city_response.status == 'success'


def add_road_to_db(client, first_city, second_city, distance, duration):
    road = Road(first_city_name=first_city, second_city_name=second_city,
                distance_km=distance, duration_minutes=duration)
    response = client.post("/road", json=road.dict())

    road_response = RoadResponse(**response.json())
    assert road_response.status == 'success'
