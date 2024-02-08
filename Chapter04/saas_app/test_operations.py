from operations import add_user, get_user
from models import User, Role


def test_add_user_into_the_database(session):
    user = add_user(
        session=session,
        username="sheldonsonny",
        password="difficultpassword",
        email="sheldonsonny@email.com",
    )

    assert (
        session.query(User)
        .filter(User.id == user.id)
        .first()
        == user
    )


def test_add_premium_user_into_the_database(session):
    user = add_user(
        session=session,
        username="mariorossi",
        password="difficultpassword",
        email="mariorossi@email.com",
        role=Role.premium,
    )

    premium_user = (
        session.query(User)
        .filter(User.id == user.id)
        .first()
    )

    assert premium_user.role == Role.premium


def test_get_user_by_username(fill_database_session):
    user = get_user(fill_database_session, "johndoe")

    assert user.username == "johndoe"
    assert user.email == "johndoe@email.com"


def test_get_user_by_email(fill_database_session):
    user = get_user(
        fill_database_session, "johndoe@email.com"
    )

    assert user.username == "johndoe"
    assert user.email == "johndoe@email.com"
