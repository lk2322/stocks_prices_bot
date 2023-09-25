import os

import pytest

from src.db import add_person, add_ticker, get_tickers, remove_ticker, initialize_db, get_person


def test_initialize_db():
    print(os.getenv("DB_URL"))
    initialize_db()


def test_add_person():
    add_person(1)
    assert get_person(1) is not None


def test_add_ticker():
    add_ticker(1, 'AAPL')
    assert get_tickers(1) == ['AAPL']


def test_add_duplicate_ticker():
    add_ticker(1, 'AAPL')
    assert get_tickers(1) == ['AAPL']


def test_remove_ticker():
    remove_ticker(1, 'AAPL')
    assert get_tickers(1) == []
