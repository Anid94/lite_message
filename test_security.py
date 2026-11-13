from security import hash_password, verify_password


def test_password():
    password_hash = hash_password("qwerty123")
    assert verify_password("qwerty123", password_hash)

def test_invalid_password():
    password_hash = hash_password("qwerty123")
    assert not verify_password("invalid00", password_hash)