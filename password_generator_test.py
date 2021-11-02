from main import generate_password, charge

def test():
    password = generate_password(True, True, "test")
    assert len(password) > 30, "password is too small"
    assert len(password) <= 50, "password is too big"
    print("everything is great")

test()
