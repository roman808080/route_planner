import http
from fastapi import APIRouter, HTTPException

from models import (City, CityResponse, Road, RoadResponse)

from db import (db_manager, is_city_in_table, is_road_in_table,
                get_city_id, delete_depended_roads)
from schema import cities, roads
from utils import (raise_http_404_if_cities_were_not_found,
                   raise_http_409_city_already_exists,
                   raise_http_404_city_not_found,
                   raise_http_409_road_already_exists,
                   raise_http_404)

router = APIRouter(prefix="/admin",
                   tags=["admin"],)


@router.post("/city")
async def add_city(city: City):
    """Add a city to the table"""

    if await is_city_in_table(name=city.name):
        raise_http_409_city_already_exists(city_name=city.name)

    query = cities.insert(
        values={"name": city.name,
                "lattitude": city.lattitude,
                "longitude": city.longitude})

    database = db_manager.get_database()
    await database.execute(query=query)

    return CityResponse(status='success')


@router.delete("/city/{name}")
async def delete_city(name: str):
    """Delete a city in the table"""
    await delete_depended_roads(city_name=name)

    query = cities.delete().where(cities.c.name == name)
    database = db_manager.get_database()
    await database.execute(query=query)

    return CityResponse(status='deleted')


@router.put("/city/{name}")
async def update_city(name: str, city: City):
    """Update a city in the table"""

    query = cities.select().where(cities.c.name == name)
    database = db_manager.get_database()

    row = await database.fetch_one(query=query)
    if row is None:
        raise_http_404_city_not_found(city_name=name)

    query = cities.update().where(cities.c.name == name).values(name=city.name,
                                                                lattitude=city.lattitude,
                                                                longitude=city.longitude)
    await database.execute(query=query)

    return CityResponse(status='updated')


@router.post("/road")
async def add_road(road: Road):
    """Add a road to the Roads table"""

    first_city_id = await get_city_id(name=road.first_city_name)
    second_city_id = await get_city_id(name=road.second_city_name)
    raise_http_404_if_cities_were_not_found([first_city_id, second_city_id])

    if await is_road_in_table(first_city_id=first_city_id,
                              second_city_id=second_city_id):
        raise_http_409_road_already_exists(first_city_name=road.first_city_name,
                                           second_city_name=road.second_city_name)

    query = roads.insert(
        values={"first_city_id": first_city_id,
                "second_city_id": second_city_id,
                "distance_km": road.distance_km,
                "duration_minutes": road.duration_minutes})

    database = db_manager.get_database()
    await database.execute(query=query)

    return RoadResponse(status='success')


@router.put("/road/{first_city}/{second_city}")
async def update_road(first_city: str, second_city: str, road: Road):
    """Update a road in the roads table"""

    first_city_id = await get_city_id(name=first_city)
    second_city_id = await get_city_id(name=second_city)
    raise_http_404_if_cities_were_not_found([first_city_id, second_city_id])

    query = roads.select().where(roads.c.first_city_id == first_city_id,
                                 roads.c.second_city_id == second_city_id)
    database = db_manager.get_database()

    row = await database.fetch_one(query=query)
    if row is None:
        road_name=f'{road.first_city_name}->{road.second_city_name}'
        raise_http_404(detail='Item not found',
                       header_error=f'Request asked for road name: [{road_name}]')

    query = roads.update().where(roads.c.first_city_id == first_city_id,
                                 roads.c.second_city_id == second_city_id).values(first_city_id=first_city_id,
                                                                                  second_city_id=second_city_id,
                                                                                  distance_km=road.distance_km,
                                                                                  duration_minutes=road.duration_minutes)
    await database.execute(query=query)

    return RoadResponse(status='updated')


@router.delete("/road/{first_city}/{second_city}")
async def delete_road(first_city: str, second_city: str):
    """Delete a city in the table"""
    first_city_id = await get_city_id(name=first_city)
    second_city_id = await get_city_id(name=second_city)
    raise_http_404_if_cities_were_not_found([first_city_id, second_city_id])

    query = roads.delete().where(roads.c.first_city_id == first_city_id,
                                 roads.c.second_city_id == second_city_id)

    database = db_manager.get_database()
    await database.execute(query=query)

    return RoadResponse(status='deleted')
