import os
import argparse
import time
from datetime import date
from cm.config import Config
from cm.client import Client

def main():
    parser = argparse.ArgumentParser(description='Export CM transactions.')
    parser.add_argument('account', help='Account id to export')
    args = parser.parse_args()

    directory = ensure_export_dir()
    start_date = last_export_date(directory)
    export(directory, args.account, start_date)

def ensure_export_dir() -> str:
    directory = Config.Transactions.directory
    if not os.path.exists(directory):
        os.makedirs(directory)
    return directory

def last_export_date(directory: str) -> date:
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    timestamps = sorted(list(map(lambda file: int(file), files)), reverse=True)
    return date.fromtimestamp(timestamps[0]) if len(timestamps) > 0 else None

def export(directory: str, account_id: str, start_date: date) -> None:
    with Client(Config.Login.username, Config.Login.password) as cm:
        cm.authenticate()
        ofx_file_name = str(int(time.time()))
        ofx_file_path = directory + '/' + ofx_file_name
        date_format = Config.Transactions.date_format
        start = start_date.strftime(date_format) if start_date else None
        cm.download_ofx_to(ofx_file_path, account_id, start)

if __name__ == '__main__':
   main()    
    
