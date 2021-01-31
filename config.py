#Simple config file. Put your USR and PWD into your environment variables

import os

def cre():
    USR = os.getenv('SO_USR')
    PWD = os.getenv('SO_PWD')

    credentials = [USR, PWD]

    return credentials

if __name__ == 'main':
    cre()
