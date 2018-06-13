import configparser

config = configparser.ConfigParser()

config.read('cm.ini')

class Config(object):

    class Login(object):
        username = config['LOGIN']['username']
        password = config['LOGIN']['password']

    class Transactions(object):
        directory = config['TRANSACTIONS']['directory']
        date_format = config['TRANSACTIONS']['dateformat']

    class Stats(object):
        db_path = config['STATS']['dbpath']
