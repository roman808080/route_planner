import http
from fastapi import HTTPException


def raise_http_error(detail: str, header_error: str, status_code: http.HTTPStatus):
    raise HTTPException(status_code=status_code,
                        detail=detail,
                        headers={"Error": header_error})


def raise_http_404(detail: str, header_error: str):
    raise_http_error(detail=detail, header_error=header_error,
                     status_code=http.HTTPStatus.NOT_FOUND)


def raise_http_404_if_cities_were_not_found(list_of_city_ids):
    for city_id in list_of_city_ids:
        if city_id is None:
            raise_http_404(detail='Item not found',
                           header_error=f'Request asked for city id: [{city_id}]')


def raise_http_404_non_existing_node(detail: str):
    raise_http_404(detail=detail, header_error=detail)


def raise_http_404_non_existing_road(detail: str):
    raise_http_404(detail=detail, header_error=detail)


def raise_http_409_city_already_exists(city_name: str):
    raise_http_error(detail=f'The city {city_name} already exists',
                     header_error=f'Request asked for city name: [{city_name}]',
                     status_code=http.HTTPStatus.CONFLICT)


def raise_http_404_city_not_found(city_name: str):
    raise_http_404(detail='Item not found',
                   header_error=f'Request asked for city name: [{city_name}]')


def raise_http_409_road_already_exists(first_city_name: str, second_city_name: str):
    raise_http_error(detail=f'The road {first_city_name}->{second_city_name} already exists',
                     header_error=f'Request asked for road name: [{first_city_name}->{second_city_name}]',
                     status_code=http.HTTPStatus.CONFLICT)
