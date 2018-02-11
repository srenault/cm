from typing import List

import requests

from simplebank.models import BankAccount


class Bank(object):
    def __init__(self):
        self.cache = {}

    def __enter__(self):
        self.session = requests.session()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()

    def _put_in_cache(self, key: str, value):
        """
        Put value in a cache to retrieve it with the _get_cached() method.
        :param key:
        :param value:
        :return:
        """
        self.cache[key] = value

    def _get_cached(self, key: str):
        try:
            return self.cache[key]
        except KeyError:
            return None

    def _is_authenticated(self) -> bool:
        """
        :return: True if the user is authenticated to the bank.
        """
        pass

    def _authenticate(self) -> None:
        """
        Authenticate the user to the bank with the informations given in the constructor.

        :raise BadAuthenticationError: if the authentication does not pass
        """
        pass

    def _authenticate_if_necessary(self) -> None:
        if not self._is_authenticated():
            self._authenticate()

    def list_accounts(self) -> List[BankAccount]:
        pass

    def fetch_last_operations(self, account_id: str) -> BankAccount:
        pass
