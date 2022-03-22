from fastapi import FastAPI

from models import RouteRequest, RouteResponse, TestResponse, City

from db_utils import Db
from schema import cities

app = FastAPI()


@app.on_event("startup")
async def startup():
    """Executed on server's startup"""
    db = Db.get_instance()
    await db.up()


@app.on_event("shutdown")
async def shutdown():
    """Executed on server's shutdown"""
    db = Db.get_instance()
    await db.down()


@app.post("/admin/city")
async def add_city(city: City):
    """Add a city to the database"""
    query = cities.insert(
        values={"name": city.name,
                "lattitude": city.lattitude,
                "longitude": city.longitude})

    database = Db.get_instance().get_database()
    last_record_id = await database.execute(query=query)

    return {**city.dict(), "id": last_record_id}


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


@app.get("/test")
async def get_test_response():
    """A test get request to make sure that everything is okay."""
    return TestResponse(test_response="Everyting is ok")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
