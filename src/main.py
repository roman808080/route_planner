from fastapi import FastAPI, HTTPException

from models import RouteRequest, RouteResponse, City, CityResponse

from db import db_manager
from schema import cities

app = FastAPI()


@app.on_event("startup")
async def startup():
    """Executed on server's startup"""
    await db_manager.up()


@app.on_event("shutdown")
async def shutdown():
    """Executed on server's shutdown"""
    await db_manager.down()


async def is_city_in_table(name):
    query = cities.select().where(cities.c.name == name)

    database = db_manager.get_database()
    rows = await database.fetch_all(query=query)
    if len(rows) > 0:
        return True

    return False


@app.post("/city")
async def add_city(city: City):
    """Add a city to the table"""

    if await is_city_in_table(name=city.name):
        return CityResponse(status='success')

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
        raise HTTPException(status_code=404,
                            detail="Item not found",
                            headers={
                                "X-Error": f"Request asked for city name: [{name}]"})

    query = cities.update().where(cities.c.name == name).values(name=city.name,
                                                                lattitude=city.lattitude,
                                                                longitude=city.longitude)
    await database.execute(query=query)

    return CityResponse(status='updated')


@app.post("/route")
async def plan_route(params: RouteRequest):
    """Plan a route between cities"""
    raise NotImplementedError()
    return RouteResponse(
        distance_km=168.43,
        duration_minutes=95,
        route=["Ostrava", "Bilovec", "Hranice",
               "Olomouc", "Prostejov", "Vyskov", "Brno"],
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
