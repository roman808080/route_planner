import pytest
from fastapi import HTTPException

from models import PlanningStrategy, RouteRequest, RouteResponse
from test_utils import add_city_to_db


async def test_route(client, prepared_database):
    route_request = RouteRequest(start="Reykjavik", destination="Belgrade",
                                 strategy=PlanningStrategy.fastest).dict()
    response = client.post("/route", json=route_request)
    route_response = RouteResponse(**response.json())

    assert route_response.distance_km == 13
    assert route_response.duration_minutes == 8

    assert route_response.route == ['Reykjavik', 'Oslo', 'Moscow', 'Belgrade']


async def test_route_with_non_existing_city(client, prepared_database):
    route_request = RouteRequest(start="Dnipro", destination="Oslo",
                                 strategy=PlanningStrategy.fastest).dict()
    response = client.post("/route", json=route_request)

    detail = response.json()['detail']

    expected_message = ("One of the nodes does not exist. "
                        "Start city = Dnipro, target city = Oslo. Start node = None, target node = 2")
    assert expected_message in detail


async def test_route_with_non_existing_road(client, prepared_database):
    add_city_to_db(client=client, name='Druzhkivka')

    route_request = RouteRequest(start="Druzhkivka", destination="Oslo",
                                 strategy=PlanningStrategy.fastest).dict()
    response = client.post("/route", json=route_request)

    detail = response.json()['detail']

    expected_message = ("The route does not exist. "
                        "Start city = Druzhkivka, target city = Oslo.")
    assert expected_message in detail
