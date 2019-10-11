from driver import Driver
from parser import Parser
import pickle

import sys
import os
import json

URL = 'https://www.ticktick.com/signin'
DRIVER_PATH = '/Users/lazyer/Lazyer/Utils/chromedriver'
JSON_FILE = 'token.json'

def get_token(json_file):
    token = json.load(open(json_file, 'r'))
    return token


if __name__ == '__main__':
    try:
        driver = Driver(path=DRIVER_PATH, debug=True)
        driver.get_url(URL)
        if driver.check_main_loaded(msg='load page'):
            print('[*]Main loded with cookie')
        else:
            token = get_token(JSON_FILE)
            if not driver.get_login(msg='login', token=token):
                print("[*]Can't login")
            if not driver.check_2nd_auth(msg='auth'):
                print("[*]Can't check 2nd auth")
            if not driver.check_main_loaded(msg='load page'):
                print("Can't not load page")
        parser = Parser(driver.get_page_source())
        main_tasks = parser.get_tasks_from_main()
        print(main_tasks)
    except Exception as e:
        print(str(e))
    finally:
        print('[*]Close driver')
        driver.close()



