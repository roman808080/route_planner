from fastapi import FastAPI

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


@app.post("/city")
async def add_city(city: City):
    """Add a city to the database"""
    query = cities.insert(
        values={"name": city.name,
                "lattitude": city.lattitude,
                "longitude": city.longitude})

    database = db_manager.get_database()
    await database.execute(query=query)

    return CityResponse(status='success')


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
