import datetime
from typing import List
from functools import reduce

from bs4 import BeautifulSoup

from simplebank.errors import BadAuthenticationError
from simplebank.api import Bank
from simplebank.models import BankAccount, BankAccountInput, BankDownloadForm


class CreditMutuel(Bank):
    BASE_URL = "https://www.creditmutuel.fr"
    AUTH_URL = BASE_URL + "/fr/authentification.html"
    DOWNLOAD_URL = BASE_URL + "/fr/banque/compte/telechargement.cgi"

    FIELD_SEPARATOR = ";"
    DATE_FORMAT = "%d/%m/%Y"

    def __init__(self, login: str, password: str):
        super().__init__()
        self.login = login
        self.password = password

    def is_authenticated(self) -> bool:
        try:
            id_session = self.session.cookies['IdSes']
            return id_session is not None and id_session != ''
        except KeyError:
            return False

    def authenticate(self) -> None:
        post_data = {
            "_cm_user": self.login,
            "_cm_pwd": self.password,
            "flag": "password"
        }
        res = self.session.post(self.AUTH_URL, post_data)
        if res.url == self.AUTH_URL:
            raise BadAuthenticationError()

    def fetch_download_form(self) -> BankDownloadForm:
        response = self.session.get(self.DOWNLOAD_URL)
        soup = BeautifulSoup(response.text, "html.parser")
        form = soup.select("#P:F")[0]
        action = form.attrs["action"]
        accounts = {}

        for account_label in soup.select("#account-table label"):
            label = account_label.text
            split = label.split(" ", maxsplit=3)
            id = "".join(split[0:3])
            check_id = account_label.attrs["for"]
            check = soup.select("#" + check_id)[0]
            check_name = check.attrs["name"]
            bank_account_input = BankAccountInput(id, label, check_id, check_name)
            accounts[id] = bank_account_input

        return BankDownloadForm(action, accounts)

    def fetch_csv(self, account_id: str) -> str:
        form = self.fetch_download_form()

        url = self.BASE_URL + form.action
        account = form.accounts[account_id]

        post_data = {
            "data_formats_selected": "csv",
            "data_formats_options_csv_fileformat": "2",
            "data_formats_options_csv_dateformat": "0",
            "data_formats_options_csv_fieldseparator": "0",
            "data_formats_options_csv_amountcolnumber": "0",
            "data_formats_options_csv_decimalseparator": "1",
            account.check_name: "on",
            "_FID_DoDownload.x": "0",
            "_FID_DoDownload.y": "0"
        }
        response = self.session.post(url, post_data)
        return response.text

    def fetch_ofx(self, account_id: str, start_date: str = "", end_date: str = "") -> str:
        form = self.fetch_download_form()

        url = self.BASE_URL + form.action
        account = form.accounts[account_id]

        post_data = {
            "data_formats_selected": "ofx",
            "data_formats_options_ofx_fileformat": "ofx-format-m2003",
            "data_daterange_value": "1",
            "[t:dbt%3adate;]data_daterange_startdate_value": start_date,
            "[t:dbt%3adate;]data_daterange_enddate_value": end_date,
            account.check_name: "on",
            "_FID_DoDownload.x": "0",
            "_FID_DoDownload.y": "0"
        }
        response = self.session.post(url, post_data)
        return response.text

    def download_ofx_to(self, path: str, account_id: str, start_date: str = "", end_date: str = "") -> None:
        content = self.fetch_ofx(account_id, start_date, end_date)
        file = open(path, "w+")
        file.write(content)
        file.close()

    def list_accounts(self) -> List[BankAccount]:
        form = self.fetch_download_form()

        accounts = []
        for _, account_input in form.accounts.items():
            balance = self.fetch_balance(account_input.id)
            accounts.append(BankAccount(account_input.id, account_input.label, balance))

        return accounts

    def fetch_balance(self, account_id: str):
        csv = self.fetch_csv(account_id)
        lines = csv.splitlines()
        last = lines.pop()
        return float(last.split(self.FIELD_SEPARATOR)[4])

    def compute_overall_balance(self) -> float:
        return reduce((lambda balance, accountB: balance + accountB.balance), self.list_accounts(), 0)
        
