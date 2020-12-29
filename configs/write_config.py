# python 3.x
from configparser import ConfigParser

config = ConfigParser()

config.add_section('main')
config.set('main', 'CLIENT_ID', '')
config.set('main', 'REDIRECT_URI', '')
config.set('main', 'JSON_PATH', '')
config.set('main', 'ACCOUNT_NUMBER', '')

with open('configs/config.ini', 'w+') as f:
    config.write(f)