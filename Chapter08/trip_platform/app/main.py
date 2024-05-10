import logging
from typing import Annotated

from fastapi import BackgroundTasks, Depends, FastAPI
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from app import internationalization
from app.background_task import (
    store_query_to_external_db,
)
from app.dependencies import (
    CommonQueryParams,
    check_coupon_validity,
    select_category,
    time_range,
)
from app.middleware import ClientInfoMiddleware
from app.profiler import router as profiler_router
from app.rate_limiter import limiter

logger = logging.getLogger("uvicorn")

app = FastAPI()


app.add_middleware(ClientInfoMiddleware)

app.include_router(internationalization.router)
app.include_router(profiler_router)

app.state.limiter = limiter
app.add_exception_handler(
    RateLimitExceeded, _rate_limit_exceeded_handler
)
app.add_middleware(SlowAPIMiddleware)


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
    background_tasks: BackgroundTasks,
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

    background_tasks.add_task(
        store_query_to_external_db, message
    )
    logger.info(
        "Query sent to background task, end of request."
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
