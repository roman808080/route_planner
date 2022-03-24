import http
from fastapi import HTTPException


def raise_http_404_if_cities_were_not_found(list_of_city_ids):
    for city_id in list_of_city_ids:
        if city_id is None:
            raise HTTPException(status_code=http.HTTPStatus.NOT_FOUND,
                                detail="Item not found",
                                headers={
                                    "Error": f"Request asked for city id: [{city_id}]"})


def raise_http_404_non_existing_node(message):
    raise HTTPException(status_code=http.HTTPStatus.NOT_FOUND,
                        detail=message,
                        headers={
                            "Error": message})


def raise_http_404_non_existing_road(message):
    raise HTTPException(status_code=http.HTTPStatus.NOT_FOUND,
                        detail=message,
                        headers={
                            "Error": message})
