import os
import argparse
from datetime import datetime
from cm.config import Config
from cm.client import Client

def main():
    parser = argparse.ArgumentParser(description='Export CM transactions.')
    parser.add_argument('accountids', help='Account ids to export', nargs='+')
    args = parser.parse_args()

    for account_id in args.accountids:
        directory = ensure_export_dir(account_id)
        start_date = last_export_date(directory)
        export(directory, account_id, start_date)

def ensure_export_dir(account_id: str) -> str:
    directory = Config.Transactions.directory + '/' + account_id
    if not os.path.exists(directory):
        os.makedirs(directory)
    return directory

def last_export_date(directory: str) -> object:
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    filtered_files = list(filter(lambda file: os.path.splitext(file)[1] == '.ofx', files))
    date_format = Config.Transactions.date_format
    dates = sorted(map(lambda file: datetime.strptime(os.path.splitext(file)[0], date_format), filtered_files), reverse=True)
    return dates[0] if dates else None

def export(directory: str, account_id: str, start_date: object) -> None:
    with Client(Config.Login.username, Config.Login.password) as cm:
        cm.authenticate()
        ofx_file_name = datetime.utcnow().strftime(Config.Transactions.date_format)
        ofx_file_path = f"{directory}/{ofx_file_name}.ofx"
        start = start_date.strftime('%Y/%m/%d') if start_date else None
        cm.download_ofx_to(ofx_file_path, account_id, start)

if __name__ == '__main__':
    main()
