from fastapi import APIRouter, Depends

from app.database import mongo_database

router = APIRouter(
    prefix="/thirdparty",
    tags=["third party"],
)


@router.get("/users/actions")
async def get_users_with_actions(
    db=Depends(mongo_database),
):
    users = [
        user
        async for user in db.users_data_view.find(
            {}, {"_id": 0}
        )
    ]

    return users
