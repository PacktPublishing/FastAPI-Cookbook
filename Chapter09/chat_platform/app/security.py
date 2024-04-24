from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Request,
    WebSocket,
    WebSocketException,
    status,
)
from fastapi.responses import HTMLResponse
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
)
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "hashed_password": "hashedsecret",
    },
    "alice": {
        "username": "alice",
        "hashed_password": "hashedsecret2",
    },
}


def fakely_hash_password(password: str):
    return f"hashed{password}"


class User(BaseModel):
    username: str


class UserInDB(User):
    hashed_password: str


def get_user(
    db: dict[str, str], username: str
) -> User | None:
    if username in db:
        user_dict = db[username]
        return User(**user_dict)


def fake_token_generator(user: UserInDB) -> str:
    # This doesn't provide any security at all
    return f"tokenized{user.username}"


def fake_token_resolver(token: str) -> UserInDB | None:
    if token.startswith("tokenized"):
        user_id = token.removeprefix("tokenized")
        user = get_user(fake_users_db, user_id)
        return user


class OAuth2PasswordBearerWebSocket(
    OAuth2PasswordBearer
):
    async def __call__(
        self, websocket: WebSocket
    ) -> str:
        authorization: str = websocket.headers.get(
            "authorization"
        )
        if not authorization:
            raise WebSocketException(
                code=status.HTTP_401_UNAUTHORIZED,
                reason="Not authenticated",
                headers={"WWW-Authenticate": "Bearer"},
            )
        scheme, param = authorization.split()
        if scheme.lower() != "bearer":
            raise WebSocketException(
                code=status.HTTP_403_FORBIDDEN,
                reason="Invalid authentication credentials",
            )
        return param


oauth2_scheme = OAuth2PasswordBearerWebSocket(
    tokenUrl="token"
)


def get_user_from_token(
    token: str = Depends(oauth2_scheme),
) -> User:
    user = fake_token_resolver(token)
    if not user:
        raise WebSocketException(
            code=status.HTTP_401_UNAUTHORIZED,
            reason="Invalid authentication credentials",
        )
    return user


router = APIRouter()


@router.post("/token")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(
            status_code=400,
            detail="Incorrect username or password",
        )
    user = UserInDB(**user_dict)
    hashed_password = fakely_hash_password(
        form_data.password
    )
    if not hashed_password == user.hashed_password:
        raise HTTPException(
            status_code=400,
            detail="Incorrect username or password",
        )

    token = fake_token_generator(user)

    return {
        "access_token": token,
        "token_type": "bearer",
    }


@router.get("/login")
async def login_form(request: Request) -> HTMLResponse:
    templates = Jinja2Templates(directory="templates")
    return templates.TemplateResponse(
        request=request,
        name="login.html",
    )
