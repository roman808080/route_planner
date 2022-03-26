from prometheus_client import Counter
from fastapi import Request

prometheus_exceptions = Counter('server_exceptions_total',
                                'Total number of exception raised by this webserver',
                                ['method', 'endpoint'])

prometheus_requirements = Counter('server_requests_total',
                                  'Total number of requests to this webserver',
                                  ['method', 'endpoint'])


async def middleware_calculate_requests(request: Request, call_next):
    prometheus_requirements.labels(method=request.method, endpoint=request.url.path).inc()

    response = await call_next(request)
    return response


async def middleware_calculate_unhandled_exceptions(request: Request, call_next):
    try:
        response = await call_next(request)
        return response

    except Exception as exc:
        prometheus_exceptions.labels(method=request.method, endpoint=request.url.path).inc()
        raise exc
