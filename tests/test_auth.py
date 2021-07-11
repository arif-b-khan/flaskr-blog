import pytest

from flask import g
from flask import session
from flaskr.db import get_db


def test_register(client, app):
    assert client.get('/auth/register').status_code == 200

    response = client.post("/auth/register", data={"username":"a", "password": "a"})
    assert response.location == "http://localhost/auth/login"

    with app.app_context():
        assert (
            get_db().execute("select * from user where username= 'a'").fetchone()
        )


