from fastapi import FastAPI

from models import RouteRequest, RouteResponse, TestResponse

app = FastAPI()


@app.post("/route")
def plan_route(params: RouteRequest):
    raise NotImplementedError()
    return RouteResponse(
        distance_km=168.43,
        duration_minutes=95,
        route=["Ostrava", "Bilovec", "Hranice",
               "Olomouc", "Prostejov", "Vyskov", "Brno"],
    )


@app.get("/test")
def get_test_response():
    return TestResponse(test_response="Everyting is ok")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
