from types import SimpleNamespace

from app.security import create_access_token, hash_password, verify_password


def test_password_hash_roundtrip():
    hashed = hash_password("TestPasswort123!")
    assert hashed != "TestPasswort123!"
    assert verify_password("TestPasswort123!", hashed)
    assert not verify_password("FalschesPasswort", hashed)


def test_access_token_is_created():
    token = create_access_token(SimpleNamespace(id=7, email="admin@example.com"))
    assert isinstance(token, str)
    assert token.count(".") == 2
