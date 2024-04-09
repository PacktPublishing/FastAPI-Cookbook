from typing import Annotated

from fastapi import Depends, FastAPI

# from fastapi.responses import HTMLResponse
# from pyinstrument import Profiler
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from app import internationalization
from app.dependencies import (
    CommonQueryParams,
    check_coupon_validity,
    select_category,
    time_range,
)
from app.middleware import ClientInfoMiddleware

# from app.rate_limiter import limiter

app = FastAPI()


app.add_middleware(ClientInfoMiddleware)

# app.state.limiter = limiter
# app.add_exception_handler(
#    RateLimitExceeded, _rate_limit_exceeded_handler
# )
# app.add_middleware(SlowAPIMiddleware)

# profiler = Profiler(
#    interval=0.001, async_mode="enabled"
# )

# TODO check how to cumulate the stats and setup the specific endpoint
# build two endpoints with some sleeping time in it
# write a test that calls both endpoints, then check the stats
# make a first improuvement by adding a worker, then another
# by using asynchrounous calls in between
# you can also profile the tests directly to show the difference
# this will probably be with timeit (to check)
# @app.middleware("http")
# async def profile_request(request: Request, call_next):
#    if request.url.path in ["/docs", "/openapi.json"]:
#        return await call_next(request)
#    profiler.start()
#    await call_next(request)
#    profiler.stop()
#    return HTMLResponse(profiler.output_html())


app.include_router(internationalization.router)


@app.get("/v1/trips")
def get_trips(
    time_range: Annotated[time_range, Depends()],
):
    start, end = time_range
    message = f"Request trips from {start}"
    if end:
        return f"{message} to {end}"
    return message


@app.get("/v2/trips/{category}")
def get_trips_by_category(
    category: Annotated[select_category, Depends()],
    discount_applicable: Annotated[
        bool, Depends(check_coupon_validity)
    ],
):
    category = category.replace("-", " ").title()
    message = f"You requested {category} trips."

    if discount_applicable:
        message += (
            "\n. The coupon code is valid! "
            "You will get a discount!"
        )
    return message


@app.get("/v3/trips/{category}")
def get_trips_by_category_v3(
    common_params: Annotated[
        CommonQueryParams, Depends()
    ],
):
    start = common_params.start
    end = common_params.end
    category = common_params.category.replace(
        "-", " "
    ).title()
    message = f"You requested {category} trips within"
    message += f" from {start}"
    if end:
        message += f" to {end}"
    if common_params.applicable_discount:
        message += (
            "\n. The coupon code is valid! "
            "You will get a discount!"
        )

    return message
