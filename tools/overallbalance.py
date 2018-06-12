from cm.client import Client
from cm.config import Config

def main():
    with Client(Config.Login.username, Config.Login.password) as cm:
        cm.authenticate()
        print(cm.compute_overall_balance())

if __name__ == '__main__':
   main()
