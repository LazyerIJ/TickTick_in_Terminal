import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from parser import Parser

URL = 'https://www.ticktick.com/signin'
DRIVER_PATH = '/Users/lazyer/Lazyer/Utils/chromedriver'


def try_until_limit(func):
    """try_until_limit
    do several times until success.
    If success func, return True else return Flase

    :param func:wrap func
    """
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


class WebDriver:
    """Driver"""
    def __init__(self, debug=False, url=URL, path=DRIVER_PATH):
        options = webdriver.ChromeOptions()
        options.add_argument('user-data-dir=selenium')
        if not debug:
            options.add_argument('headless')
        self.driver = webdriver.Chrome(path, chrome_options=options)
        self.driver.get(url)
        
        self.set_tab('project')

    @try_until_limit
    def check_2nd_auth(self, msg, limit):
        return not self.driver.find_elements_by_id('headingText')

    @try_until_limit
    def check_main_loaded(self, msg, limit):
        return self.driver.find_elements_by_class_name('username')

    @try_until_limit
    def check_task_list(self, msg, limit):
        return self.driver.find_elements_by_id('task-list-view')


    @try_until_limit
    def input_userinfo(self, msg, token, limit):
        """login

        :param msg: print msg
        :param token: {google id, google password}
        :param limit: how many try
        """
        try:
            wait = WebDriverWait(self.driver, 2)
            #find google login
            element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'google')))
            element.click()
            #find input email
            email_input = wait.until(EC.presence_of_element_located((By.NAME, 'identifier')))
            email_input.send_keys(token['email'])
            element = wait.until(EC.presence_of_element_located((By.ID, 'identifierNext')))
            element.send_keys('\n')
            #find input password
            pw_input = wait.until(EC.presence_of_element_located((By.NAME, 'password')))
            pw_input.send_keys(token['password'])
            element = wait.until(EC.presence_of_element_located((By.ID, 'passwordNext')))
            element.send_keys('\n')
            #wait main page load
            element = wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
            return True

        except Exception as e:
            return False

    def close(self):
        self.driver.close()

    def restart(self):
        self.__init__()

    ########smart view area######
    def set_smart_view(self):
        smart_view_section_area = self.driver.find_element_by_id('smart-project-view-area')
        smart_view_sections = smart_view_section_area.find_elements_by_class_name('project')

        self.smart_view_sections_lists = {}
        for section in smart_view_sections:
            text = Parser.get_smart_list_title(section.get_attribute('innerHTML'))
            self.smart_view_sections_lists[text] = section
    
    ########project view area######
    def set_tab(self, project):
        self.selected_tab = project

    def set_project_view(self):
        project_view = self.driver.find_element_by_id('project-view-area')
        current_tab = self.selected_tab
        current_tag = self.get_tab_tag()
        project_view.find_element_by_class_name(current_tag).click()

        self.project_view_sections_lists = {}
        project_list = self.driver.find_element_by_class_name('project-list')
        for project in project_list.find_elements_by_class_name('project-link'):
            title = Parser.get_project_list_title(project.get_attribute('innerHTML'))
            self.project_view_sections_lists[title] = project

    def get_tab_tag(self):
        if self.selected_tab == 'project':
            return 'l-tab-project'
        if self.selected_tab == 'tag':
            return 'l-tab-tag'
        if self.selected_tab == 'csl':
            return 'l-tab-csl'

    @property
    def page_source(self):
        return self.driver.page_source


