from account import hash_password, compare_password


def test_hash_compare_password():
    password = "some_test_password"
    hashed = hash_password(password)

    assert hashed != password
    assert compare_password(password, hashed) == True
    assert compare_password("wrong_password", hashed) == False


if __name__ == "__main__":
    test_hash_compare_password()
