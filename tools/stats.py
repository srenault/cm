import os
import sqlite3
from datetime import date

from cm.config import Config
from cm.client import Client

def main():
    with_db(stats)

def stats(sql_c):
    ensure_schema(sql_c)
    with Client(Config.Login.username, Config.Login.password) as cm_client:
        cm_client.authenticate()
        for account in cm_client.list_accounts():
            insert(sql_c, account.id, account.balance)

def with_db(block):
    db_file = Config.Stats.db_path
    ensure_db_dir(os.path.dirname(Config.Stats.db_path))
    conn = sqlite3.connect(db_file)
    block(conn.cursor())
    conn.commit()
    conn.close()    

def ensure_db_dir(directory: str) -> str:
    if not os.path.exists(directory):
        os.makedirs(directory)
    return directory

def insert(sql_c, account_id: str, balance: float) -> None:
    today = date.today()
    balance_id = f"{account_id}#{today.day}#{today.month}#{today.year}"
    balance_date = date.strftime(today, '%Y-%m-%d')
    sql_c.execute("INSERT INTO balances VALUES (?,?,?,?,?,?,?)", (balance_id, account_id, balance_date, today.year, today.month, today.day, balance))

def ensure_schema(sql_c) -> None:
    sql_c.execute('''CREATE TABLE IF NOT EXISTS balances (id text, account_id text, date date, year integer, month integer, day integer, balance real);''')
    sql_c.execute('''CREATE UNIQUE INDEX IF NOT EXISTS `balances_id` ON `balances` (`id`);''')
    sql_c.execute('''CREATE INDEX IF NOT EXISTS `balances_accountid` ON `balances` (`account_id`);''')
    sql_c.execute('''CREATE INDEX IF NOT EXISTS `balances_date` ON `balances` (`date`);''')
    sql_c.execute('''CREATE INDEX IF NOT EXISTS `balances_year` ON `balances` (`year`);''')
    sql_c.execute('''CREATE INDEX IF NOT EXISTS `balances_month` ON `balances` (`month`);''')
    sql_c.execute('''CREATE INDEX IF NOT EXISTS `balances_day` ON `balances` (`day`);''')
    sql_c.execute('''CREATE INDEX IF NOT EXISTS `balances_balance` ON `balances` (`balance`);''')

if __name__ == '__main__':
    main()
