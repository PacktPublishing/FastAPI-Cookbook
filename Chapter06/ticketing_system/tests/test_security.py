import pytest
from sqlalchemy import select

from app.database import CreditCard
from app.security import (
    retrieve_credit_card_info,
    store_credit_card_info,
)


async def test_store_credit_card_info(db_session_test):
    # Store encrypted credit card information in the database
    credit_card_id = await store_credit_card_info(
        db_session_test,
        card_number="1234567812345678",
        card_holder_name="John Doe",
        expiration_date="12/23",
        cvv="123",
    )
    assert credit_card_id is not None


@pytest.fixture
async def get_credit_card_id(db_session_test):
    credit_card_id = await store_credit_card_info(
        db_session_test,
        card_number="1234567812345678",
        card_holder_name="John Doe",
        expiration_date="12/23",
        cvv="123",
    )
    return credit_card_id


async def test_retrieve_credit_card_info(
    db_session_test, get_credit_card_id
):
    credit_card = await retrieve_credit_card_info(
        db_session_test, get_credit_card_id
    )
    assert (
        credit_card["card_number"] == "1234567812345678"
    )
    assert credit_card["card_holder_name"] == "John Doe"
    assert credit_card["expiration_date"] == "12/23"

    query = select(CreditCard).where(
        CreditCard.id == get_credit_card_id
    )

    async with db_session_test as session:
        result = await session.execute(query)
        credit_card = result.scalars().first()
    assert credit_card.cvv != "123"
    assert credit_card.number != "1234567812345678"
