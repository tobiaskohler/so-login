#Short and handy script to login and after "x" seconds logout from Stackoverflow
import requests
import config
import re
import datetime
import time


### DEFINING VARIABLES ###
headers = {
    'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8',
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
}

params = {
    "ssrc": "head",
    "returnurl": "https://stackoverflow.com/",
}

url = 'https://stackoverflow.com/users/login?ssrc=head&returnurl=https://stackoverflow.com/'

cre = config.cre()
usr = cre['USR']
pwd = cre['PWD']


### DEFINING functions ###
def find_fkey():
    print('Searching for fkey...')
    response = requests.get(url, params=params, headers=headers)
    return re.search(r'"fkey":"([^"]+)"', response.text).group(1)

def get_payload():
    fkey = find_fkey()
    return {
        'openid_identifier': '',
        'password': pwd,
        'fkey': fkey,
        'email': usr,
        'oauth_server': '',
        'oauth_version': '',
        'openid_username': '',
        'ssrc': 'head',
    }

def get_profile_url(session):
    response = session.get("https://stackoverflow.com/")
    html = response.text
    profile_url = "https://stackoverflow.com" + re.search(r'<a href="(.+)" class="my-profile', html).group(1)
    print('\033[92m Logged into profile: {} \033m'.format(profile_url))
    return profile_url


def surfing(session, profile_url):
    print('\033[92m Begin surfing...\033[0m')

    url1 = 'https://stackoverflow.com/jobs/companies'
    url2 = 'https://stackoverflow.com/questions'
    url3 = 'https://stackoverflow.com/questions/927358/how-do-i-undo-the-most-recent-local-commits-in-git'
    preference_url = 'https://stackoverflow.com/users/preferences/'
    user_id = profile_url.split('/')
    user_id = user_id[4]
    url4 = f'{preference_url}{user_id}'

    l = [url1, url2, url3, url4, url2, url1]

    for elem in l:
        stat = session.get(elem)
        print(f'Accessing {elem}....Status: {stat.status_code}')
        time.sleep(10)
    print('\033[92m Surfing successfully executed! \033')


def login():
    session = requests.session()
    print('Start login ...')
    payload = get_payload()
    response = session.post(url, data=payload, headers=headers, params=params)
    time.sleep(7)
    if response.history:
        print("\033[92m Successfully logged in: {} with fkey: {}\033[0m".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                                                                 payload['fkey']))
        profile_url = get_profile_url(session)
        session.get(profile_url)
        surfing(session, profile_url)

    else:
        print('\033[31m Something went wrong, please check again maybe USR or PWD? \033[0m')




if __name__ == '__main__':
    z = 0

    while z < 9:
        try:
            login()
            z = 9
            time.sleep(5)
        except Exception as e:
            z += 1
            print(e)
            time.sleep(5)
