import os
import sqlite3
from datetime import date

from cm.config import Config
from cm.client import Client

def main():
    with_db(stats)

def stats(c):
    ensure_schema(c)
    with Client(Config.Login.username, Config.Login.password) as cm:
        cm.authenticate()

        for account in cm.list_accounts():
            insert(c, account.id, account.balance)

def with_db(block):
    db_file = Config.Stats.db_path
    ensure_db_dir(os.path.dirname(Config.Stats.db_path))
    conn = sqlite3.connect(db_file)
    block(conn.cursor())
    conn.commit()
    conn.close()    

def ensure_db_dir(directory) -> str:
    if not os.path.exists(directory):
        os.makedirs(directory)
    return directory

def insert(c, account_id: str, balance: float) -> None:
    today = date.today()
    c.execute("INSERT INTO balances VALUES (?,?,?,?,?)", (account_id, today.year, today.month, today.day, balance))

def ensure_schema(c) -> None:
    c.execute('''CREATE TABLE IF NOT EXISTS balances (account_id text, year integer, month integer, day integer, balance real);''')
    c.execute('''CREATE INDEX `balances_accountid` ON `balances` (`account_id`);''')
    c.execute('''CREATE INDEX `balances_year` ON `balances` (`year`);''')
    c.execute('''CREATE INDEX `balances_month` ON `balances` (`month`);''')
    c.execute('''CREATE INDEX `balances_day` ON `balances` (`day`);''')
    c.execute('''CREATE INDEX `balances_balance` ON `balances` (`balance`);''')

if __name__ == '__main__':
    main()
