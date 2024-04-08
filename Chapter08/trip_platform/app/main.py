from typing import Annotated

from fastapi import Depends, FastAPI

from app import localization
from app.dependencies import (
    CommonQueryParams,
    check_coupon_validity,
    select_category,
    time_range,
)
from app.middleware import MyMiddleware

app = FastAPI()


app.add_middleware(MyMiddleware)


app.include_router(localization.router)


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
    time_range: Annotated[time_range, Depends()],
    discount_applicable: Annotated[
        bool, Depends(check_coupon_validity)
    ],
):
    start, end = time_range
    category = category.replace("-", " ").title()
    message = f"You requested {category} trips wihtin"
    message += f" from {start}"
    if end:
        message += f" to {end}"
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
