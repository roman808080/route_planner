from fastapi import FastAPI
from starlette_exporter import PrometheusMiddleware, handle_metrics

from models import RouteRequest, RouteResponse

from db import db_manager
from utils import raise_http_404_non_existing_node, raise_http_404_non_existing_road
from dijkstra_adapter import DijkstraAdapter, NonExistingNode, RouteDoesNotExist

import admin_router

APPLICATION_DEFAULT_PORT = 8000
APPLICATION_NAME = "api"

app = FastAPI()

app.add_middleware(PrometheusMiddleware, app_name=APPLICATION_NAME,
                   group_paths=True, prefix=APPLICATION_NAME)

app.add_route("/metrics", handle_metrics)
app.include_router(admin_router.router)


@app.on_event("startup")
async def startup():
    """Executed on server's startup"""
    await db_manager.up()


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
