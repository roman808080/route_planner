import http
from fastapi import HTTPException


def raise_http_404_if_cities_were_not_found(list_of_city_ids):
    for city_id in list_of_city_ids:
        if city_id is None:
            raise HTTPException(status_code=http.HTTPStatus.NOT_FOUND,
                                detail="Item not found",
                                headers={
                                    "X-Error": f"Request asked for city id: [{city_id}]"})
