from cm.client import Client
from cm.config import Config

def main():
    with Client(Config.Login.username, Config.Login.password) as cm:
        cm.authenticate()
        for account in cm.list_accounts():
            print(f"{account.label} | {account.id} | {account.balance}")

if __name__ == '__main__':
   main()
