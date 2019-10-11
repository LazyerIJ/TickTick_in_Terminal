from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def try_until_limit(func):
    def wrapper(*args, **kwargs):
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
    def __init__(self, path, debug=False):
        options = webdriver.ChromeOptions()
        options.add_argument('user-data-dir=selenium')
        if not debug:
            options.add_argument('headless')
        self.driver = webdriver.Chrome(path, chrome_options=options)

    def get_url(self, url):
        self.driver.get(url)

    @try_until_limit
    def get_login(self, msg, token):
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

    @try_until_limit
    def check_2nd_auth(self, msg):
        return not self.driver.find_elements_by_id('headingText')

    @try_until_limit
    def check_main_loaded(self, msg):
        return self.driver.find_elements_by_class_name('username')

    def get_page_source(self):
        return self.driver.page_source

    def close(self):
        self.driver.close()
