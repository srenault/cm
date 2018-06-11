import datetime
from typing import List

from bs4 import BeautifulSoup

from simplebank.errors import BadAuthenticationError
from simplebank.api import Bank
from simplebank.models import BankAccount, BankOperation


class CreditMutuel(Bank):
    BASE_URL = "https://www.creditmutuel.fr"
    AUTH_URL = BASE_URL + "/fr/authentification.html"
    FETCH_CSV_URL = BASE_URL + "/fr/banque/compte/telechargement.cgi"

    FIELD_SEPARATOR = ";"
    DATE_FORMAT = "%d/%m/%Y"

    def __init__(self, login: str, password: str):
        super().__init__()
        self.login = login
        self.password = password

    def _is_authenticated(self) -> bool:
        try:
            id_session = self.session.cookies['IdSes']
            return id_session is not None and id_session != ''
        except KeyError:
            return False

    def _authenticate(self) -> None:
        post_data = {
            "_cm_user": self.login,
            "_cm_pwd": self.password,
            "flag": "password"
        }
        res = self.session.post(self.AUTH_URL, post_data)
        if res.url == self.AUTH_URL:
            raise BadAuthenticationError()

    def _fetch_informations_and_cache_it_if_necessary(self) -> None:
        if self._get_cached('url_post_csv') is None:
            self._authenticate_if_necessary()

            # Retrieve URL to download the csv file where there is all the informations we need
            r = self.session.get(self.FETCH_CSV_URL)
            soup = BeautifulSoup(r.text, "html.parser")
            form = soup.select("#P:F")[0]
            self._put_in_cache('url_post_csv', form.attrs["action"])

            # Retrieve accounts list to match the account_id argument
            accounts = []
            for account_label in soup.select("#account-table label"):
                split = account_label.text.split(" ", maxsplit=3)
                account_number = "".join(split[0:3])
                accounts.append({'id': account_number, 'label': account_label.text})
                account_check_id = account_label.attrs["for"]
                account_check = soup.select("#" + account_check_id)[0]
                account_check_name = account_check.attrs["name"]
                self._put_in_cache('account_' + account_number + '_check_name', account_check_name)
            self._put_in_cache('accounts', accounts)

    def _fetch_csv(self, account_id: str) -> str:
        if self._get_cached('csv_' + account_id) is None:
            self._fetch_informations_and_cache_it_if_necessary()

            # Retrieve informations from cache
            url = self.BASE_URL + self._get_cached('url_post_csv')
            account_check_name = self._get_cached('account_' + account_id + '_check_name')

            # Download the file
            post_data = {
                "data_formats_selected": "csv",
                "data_formats_options_csv_fileformat": "2",
                "data_formats_options_csv_dateformat": "0",
                "data_formats_options_csv_fieldseparator": "0",
                "data_formats_options_csv_amountcolnumber": "0",
                "data_formats_options_csv_decimalseparator": "1",
                account_check_name: "on",
                "_FID_DoDownload.x": "0",
                "_FID_DoDownload.y": "0"
            }
            r = self.session.post(url, post_data)
            self._put_in_cache('csv_' + account_id, r.text)
            return r.text
        else:
            return self._get_cached('csv_' + account_id)

    def _fetch_ofx(self, account_id: str) -> str:
        self._fetch_informations_and_cache_it_if_necessary()

        # Retrieve informations from cache
        url = self.BASE_URL + self._get_cached('url_post_csv')
        account_check_name = self._get_cached('account_' + account_id + '_check_name')

        # Download the file
        post_data = {
            "data_formats_selected": "csv",
            "data_formats_options_csv_fileformat": "2",
            "data_formats_options_csv_dateformat": "0",
            "data_formats_options_csv_fieldseparator": "0",
            "data_formats_options_csv_amountcolnumber": "0",
            "data_formats_options_csv_decimalseparator": "1",
            account_check_name: "on",
            "_FID_DoDownload.x": "0",
            "_FID_DoDownload.y": "0"
        }
        r = self.session.post(url, post_data)
        return r.text

    def list_accounts(self) -> List[BankAccount]:
        self._fetch_informations_and_cache_it_if_necessary()

        accounts = []
        cached_info = self._get_cached('accounts')
        for account in cached_info:
            accounts.append(BankAccount(account['id'], account['label']))

        return accounts

    def fetch_last_operations(self, account_id: str) -> BankAccount:
        csv = self._fetch_csv(account_id)
        lines = csv.splitlines()
        operations = []

        for line in lines[1:]:
            field = line.split(self.FIELD_SEPARATOR)
            operation = BankOperation(
                datetime.datetime.strptime(field[0], self.DATE_FORMAT).date(),
                datetime.datetime.strptime(field[1], self.DATE_FORMAT).date(),
                field[3],
                float(field[2])
            )
            operations.append(operation)

        accounts = self.list_accounts()
        for account in accounts:
            if account.id == account_id:
                account.balance = self._fetch_balance(account_id)
                account.operations = operations
                return account

    def _fetch_balance(self, account_id: str):
        csv = self._fetch_csv(account_id)
        lines = csv.splitlines()
        last = lines.pop()
        return float(last.split(self.FIELD_SEPARATOR)[4])
