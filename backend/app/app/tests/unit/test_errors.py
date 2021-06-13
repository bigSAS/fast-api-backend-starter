from app.errors.api import ApiError, AuthError


def test_api_error():
    err = ApiError('foo', 400)
    print(err)

    assert err.status_code == 400
    assert err.message == 'foo'

    print("done")

    auth_err = AuthError('invalid username')
    print('.')
