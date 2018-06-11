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
    def __init__(self, id: str, label: str, balance: float = None) -> None:
        self.id = id
        self.label = label
        self.balance = balance

    def __repr__(self) -> str:
        return str(self.__dict__)

class BankAccountInput(object):
    def __init__(self, id: int, label: str, check_id: str, check_name: str) -> None:
                 self.id = id
                 self.label = label
                 self.check_id = check_id
                 self.check_name = check_name

    def __repr__(self) -> str:
        return str(self.__dict__)

class BankDownloadForm(object):
    def __init__(self, action: str, accounts: object) -> None:
                 self.action = action
                 self.accounts = accounts

    def __repr__(self) -> str:
        return str(self.__dict__)
                 
