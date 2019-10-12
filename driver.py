from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time, json, os, signal

URL = 'https://www.ticktick.com/signin'
DRIVER_PATH = '/Users/lazyer/Lazyer/Utils/chromedriver'
JSON_FILE = 'token.json'

def _get_token(json_file):
    token = json.load(open(json_file, 'r'))
    return token

def try_until_limit(func):
    def wrapper(*args, **kwargs):
        print(kwargs)
        limit = kwargs.get('limit', 10)
        sleep = kwargs.get('sleep', 2)
        step = 0
        while step < limit:
            print('[*]Waiting {}.. {}/{}'.format(kwargs['msg'], step, limit))
            if not func(*args, **kwargs):
                time.sleep(sleep)
                step += 1
            else:
                return True
        return False
    return wrapper


class Driver:
    def __init__(self, debug=False, url=URL, path=DRIVER_PATH):
        options = webdriver.ChromeOptions()
        options.add_argument('user-data-dir=selenium')
        if not debug:
            options.add_argument('headless')
        self.driver = webdriver.Chrome(path, chrome_options=options)
        self.status = None
        self.url = url

    def get_url(self):
        self.driver.get(self.url)

    @try_until_limit
    def get_login(self, msg, token ,limit=10):
        try:
            wait = WebDriverWait(self.driver, 2)

            #select Google login
            #driver.find_element_by_class_name('google').click()  # Google login
            element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'google')))
            element.click()

            #email_input = driver.find_element_by_name('identifier')
            email_input = wait.until(EC.presence_of_element_located((By.NAME, 'identifier')))
            email_input.send_keys(token['email'])
            #driver.find_element_by_id('adentifierNext').click()  # 다음
            element = wait.until(EC.presence_of_element_located((By.ID, 'identifierNext')))
            element.send_keys('\n')

            #pw_input = driver.find_element_by_name('password')
            pw_input = wait.until(EC.presence_of_element_located((By.NAME, 'password')))
            pw_input.send_keys(token['password'])
            #driver.find_element_by_id('passwordNext').click()  # 다음
            element = wait.until(EC.presence_of_element_located((By.ID, 'passwordNext')))
            element.send_keys('\n')


            element = wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
            print('[*]Load body completed')
            return True

        except Exception as e:
            print(str(e))
            return False

    def set_status(self, status):
        self.status = status

    def init_main(self):
        self.get_url()
        if self.check_main_loaded(msg='load page', limit=2):
            print('[*]Main loded with cookie')
        else:
            token = _get_token(JSON_FILE)
            if not self.get_login(msg='login', token=token):
                print("[*]Can't login")
            if not self.check_2nd_auth(msg='auth'):
                print("[*]Can't check 2nd auth")
            if not self.check_main_loaded(msg='load page'):
                print("Can't not load page")

        if self.check_task_list(msg='load task'):
            self.set_status('main')

    @try_until_limit
    def check_2nd_auth(self, msg, limit=10):
        return not self.driver.find_elements_by_id('headingText')

    @try_until_limit
    def check_main_loaded(self, msg, limit=10):
        return self.driver.find_elements_by_class_name('username')

    @try_until_limit
    def check_task_list(self, msg, limit=10):
        return self.driver.find_elements_by_id('task-list-view')

    def get_page_source(self):
        return self.driver.page_source

    def close(self):
        self.driver.close()


    def kill(self):
        pid = None
        import psutil
        for process in psutil.process_iter():
            if process.cmdline()[0] == DRIVER_PATH:
                pid = process.pid
        if pid:
            os.kill(pid, signal.SIGTERM)
        self.driver = None

    def check_alive(self):
        try:
            title = self.driver.title
            return True
        except:
            return False

    def restart(self):
        self.__init__()
