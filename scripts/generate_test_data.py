import requests
import random

MAX_CITIES_AMOUNT = 500
BASE_CITY_NAME = 'TestCity'

MIN_WEIGHT = 1
MAX_WEIGHT = 100

CHUNK_SIZE = 20
NUMBER_OF_GENERATION_CIRCLES = 3


def generate_cities():
    cities = []

    for i in range(MAX_CITIES_AMOUNT):
        city_name = f'{BASE_CITY_NAME}{i}'
        cities.append(city_name)

        json_data = {'name': city_name,
                     'lattitude': 0, 'longitude': 0}
        response = requests.post(
            'http://localhost:8000/admin/city', json=json_data).json()
        print(response)

    return cities


def generate_roads_for_shuffled_cities(cities):
    for i in range(1, len(cities)):
        start_city = cities[i -1]
        destination = cities[i]

        distance = random.randrange(MIN_WEIGHT, MAX_WEIGHT)
        duration = random.randrange(MIN_WEIGHT, MAX_WEIGHT)
        json_data = {"first_city_name": start_city,
                     "second_city_name": destination,
                     "distance_km": distance,
                     "duration_minutes": duration}

        response = requests.post('http://localhost:8000/admin/road', json=json_data)
        print(response.json())


def generate_roads_in_chunks(cities):
    rest_of_cities = cities[:]

    current_chunk, rest_of_cities = (rest_of_cities[:CHUNK_SIZE],
                                     rest_of_cities[CHUNK_SIZE:])

    while len(current_chunk) != 0:
        generate_roads_for_shuffled_cities(cities=current_chunk)
        current_chunk, rest_of_cities = rest_of_cities[:CHUNK_SIZE], rest_of_cities[CHUNK_SIZE:]
        print('The size = ', len(rest_of_cities))


def generate_random_roads(cities):
    for i in range(NUMBER_OF_GENERATION_CIRCLES):
        print("Current circle of generation is ", i + 1)
        random.shuffle(cities)
        generate_roads_in_chunks(cities=cities)


def main():
    cities = generate_cities()
    generate_random_roads(cities=cities)


if __name__ == "__main__":
    main()
