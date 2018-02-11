import datetime
from typing import List


class BankOperation(object):
    def __init__(self, date_completed: datetime.date, date_posted: datetime.date, label: str, amount: float) -> None:
        self.date_completed = date_completed
        self.date_posted = date_posted
        self.label = label
        self.amount = amount

    def __repr__(self) -> str:
        return str(self.__dict__)


class BankAccount(object):
    def __init__(self, account_id: str, label: str, balance: float = None,
                 operations: List[BankOperation] = None) -> None:
        self.id = account_id
        self.label = label
        self.balance = balance
        self.operations = operations

    def __repr__(self) -> str:
        return str(self.__dict__)
