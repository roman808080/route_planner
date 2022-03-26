from fastapi import FastAPI
from prometheus_client import start_http_server

from models import RouteRequest, RouteResponse

from db import db_manager
from schema import cities, roads
from utils import raise_http_404_non_existing_node, raise_http_404_non_existing_road
from dijkstra_adapter import DijkstraAdapter, NonExistingNode, RouteDoesNotExist
from prometheus_measurements import middleware_calculate_requests, middleware_calculate_unhandled_exceptions

import admin_router

app = FastAPI()

app.middleware("http")(middleware_calculate_requests)
app.middleware("http")(middleware_calculate_unhandled_exceptions)

app.include_router(admin_router.router)

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
        raise_http_404_non_existing_node(detail=repr(exc))
    except RouteDoesNotExist as exc:
        raise_http_404_non_existing_road(detail=repr(exc))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=APPLICATION_DEFAULT_PORT)
