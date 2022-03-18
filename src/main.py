from fastapi import FastAPI

from models import RouteRequest, RouteResponse

app = FastAPI()


@app.post("/route")
def plan_route(params: RouteRequest):
    raise NotImplementedError()
    return RouteResponse(
        distance_km=168.43,
        duration_minutes=95,
        route=["Ostrava", "Bilovec", "Hranice", "Olomouc", "Prostejov", "Vyskov", "Brno"],
    )
