import pytest
from models import PlanningStrategy, RouteRequest


async def test_route(client):
    with pytest.raises(NotImplementedError):
        response = client.post(
            "/route", json=RouteRequest(start="Ostrava", destination="Brno", strategy=PlanningStrategy.fastest).dict()
        )
