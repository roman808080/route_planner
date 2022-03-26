import http
from fastapi import FastAPI, HTTPException
from prometheus_client import start_http_server

from models import (RouteRequest, RouteResponse, City,
                    CityResponse, Road, RoadResponse)

from db import (db_manager, is_city_in_table, is_road_in_table,
                get_city_id, delete_depended_roads)
from schema import cities, roads
from utils import (raise_http_404_if_cities_were_not_found,
                   raise_http_404_non_existing_node, raise_http_404_non_existing_road)
from dijkstra_adapter import DijkstraAdapter, NonExistingNode, RouteDoesNotExist
from prometheus_measurements import middleware_calculate_requests, middleware_calculate_unhandled_exceptions

app = FastAPI()

app.middleware("http")(middleware_calculate_requests)
app.middleware("http")(middleware_calculate_unhandled_exceptions)

APPLICATION_DEFAULT_PORT = 8000
PROMETHEUS_DEFAULT_PORT = 8001


@app.on_event("startup")
async def startup():
    """Executed on server's startup"""
    await db_manager.up()
    start_http_server(PROMETHEUS_DEFAULT_PORT)


@app.on_event("shutdown")
async def shutdown():
    """Executed on server's shutdown"""
    await db_manager.down()


@app.post("/city")
async def add_city(city: City):
    """Add a city to the table"""

    if await is_city_in_table(name=city.name):
        raise HTTPException(status_code=http.HTTPStatus.CONFLICT,
                            detail=f"The city {city.name} already exists",
                            headers={
                                "X-Error": f"Request asked for city name: [{city.name}]"})

    query = cities.insert(
        values={"name": city.name,
                "lattitude": city.lattitude,
                "longitude": city.longitude})

    database = db_manager.get_database()
    await database.execute(query=query)

    return CityResponse(status='success')


@app.delete("/city/{name}")
async def delete_city(name: str):
    """Delete a city in the table"""
    await delete_depended_roads(city_name=name)

    query = cities.delete().where(cities.c.name == name)
    database = db_manager.get_database()
    await database.execute(query=query)

    return CityResponse(status='deleted')


@app.put("/city/{name}")
async def update_city(name: str, city: City):
    """Update a city in the table"""

    query = cities.select().where(cities.c.name == name)
    database = db_manager.get_database()

    row = await database.fetch_one(query=query)
    if row is None:
        raise HTTPException(status_code=http.HTTPStatus.NOT_FOUND,
                            detail="Item not found",
                            headers={
                                "X-Error": f"Request asked for city name: [{name}]"})

    query = cities.update().where(cities.c.name == name).values(name=city.name,
                                                                lattitude=city.lattitude,
                                                                longitude=city.longitude)
    await database.execute(query=query)

    return CityResponse(status='updated')


@app.post("/road")
async def add_road(road: Road):
    """Add a road to the Roads table"""

    first_city_id = await get_city_id(name=road.first_city_name)
    second_city_id = await get_city_id(name=road.second_city_name)
    raise_http_404_if_cities_were_not_found([first_city_id, second_city_id])

    if await is_road_in_table(first_city_id=first_city_id,
                              second_city_id=second_city_id):
        raise HTTPException(status_code=http.HTTPStatus.CONFLICT,
                            detail=f"The road {road.first_city_name}->{road.second_city_name} already exists",
                            headers={
                                "Error": f"Request asked for road name: [{road.first_city_name}->{road.second_city_name}]"})

    query = roads.insert(
        values={"first_city_id": first_city_id,
                "second_city_id": second_city_id,
                "distance_km": road.distance_km,
                "duration_minutes": road.duration_minutes})

    database = db_manager.get_database()
    await database.execute(query=query)

    return RoadResponse(status='success')


@app.put("/road/{first_city}/{second_city}")
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
        raise HTTPException(status_code=http.HTTPStatus.NOT_FOUND,
                            detail="Item not found",
                            headers={
                                "Error": f"Request asked for road name: [{road.first_city_name}->{road.second_city_name}]"})

    query = roads.update().where(roads.c.first_city_id == first_city_id,
                                 roads.c.second_city_id == second_city_id).values(first_city_id=first_city_id,
                                                                                  second_city_id=second_city_id,
                                                                                  distance_km=road.distance_km,
                                                                                  duration_minutes=road.duration_minutes)
    await database.execute(query=query)

    return RoadResponse(status='updated')


@app.delete("/road/{first_city}/{second_city}")
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


@app.post("/route")
async def plan_route(params: RouteRequest):
    """Plan a route between cities"""
    try:
        route_planner = DijkstraAdapter(start_city=params.start,
                                        target_city=params.destination,
                                        strategy=params.strategy)
        route, distance, duration = await route_planner.get_optimal_path()

        return RouteResponse(distance_km=distance, duration_minutes=duration,
                             route=route)

    except NonExistingNode as exc:
        raise_http_404_non_existing_node(message=repr(exc))
    except RouteDoesNotExist as exc:
        raise_http_404_non_existing_road(message=repr(exc))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=APPLICATION_DEFAULT_PORT)
