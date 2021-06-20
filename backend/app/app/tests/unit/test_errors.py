from dataclasses import dataclass
from typing import NamedTuple

from app.errors.api import ApiError, AuthError


def test_api_error():
    err = ApiError('foo', 400)
    print(err)

    assert err.status_code == 400
    assert err.message == 'foo'

    print("done")

    auth_err = AuthError('invalid username')
    print('.')


@dataclass(frozen=True)
class AccountBalance:  #NamedTuple
    """
    python value object example
    """
    amount: float
    currency: str

    def add(self, amount: float):
        new_amount = self.amount + amount
        return AccountBalance(amount=new_amount, currency=self.currency)


def test_money():
    m = AccountBalance(amount=20.20, currency='USD')
    m.add(10.234)

    m1 = AccountBalance(amount=20.2, currency='USD')
    m2 = AccountBalance(amount=20, currency='PLN')

    assert m1 == m

    assert m1 != m2
