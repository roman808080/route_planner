from fastapi import FastAPI

from models import RouteRequest, RouteResponse, TestResponse, City

from db_utils import database, create_all_tables
from schema import cities, metadata

app = FastAPI()


@app.on_event("startup")
async def startup():
    """Executed on server's startup"""
    await create_all_tables(metadata=metadata)
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    """Executed on server's shutdown"""
    await database.disconnect()


@app.post("/admin/city")
async def add_city(city: City):
    query = cities.insert(
        values={"name": city.name,
                "lattitude": city.lattitude,
                "longitude": city.longitude})
    last_record_id = await database.execute(query=query)
    return {**city.dict(), "id": last_record_id}


@app.post("/route")
async def plan_route(params: RouteRequest):
    raise NotImplementedError()
    return RouteResponse(
        distance_km=168.43,
        duration_minutes=95,
        route=["Ostrava", "Bilovec", "Hranice",
               "Olomouc", "Prostejov", "Vyskov", "Brno"],
    )


@app.get("/test")
async def get_test_response():
    return TestResponse(test_response="Everyting is ok")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
