from parser import Parser
from util import get_token

JSON_FILE = 'token.json'

class Controller:
    def __init__(self, webdriver):
        self.webdriver = webdriver
        self.smart_projects = {}

    def login(self):
        if self.webdriver.check_main_loaded(msg='load page', limit=2):
            pass
        else:
            token = get_token(JSON_FILE)
            msg = "login"
            if not self.webdriver.input_userinfo(msg=msg, token=token, limit=10):
                return False, msg 
            msg = "2nd auth"
            if not self.webdriver.check_2nd_auth(msg=msg, limit=10):
                return False, msg
            msg = "load main"
            if not self.webdriver.check_main_loaded(msg=msg, limit=10):
                return False, msg
        msg = "load task"
        if not self.webdriver.check_task_list(msg=msg, limit=2):
            return False, msg 
        return True, None

    def get_main_task(self):
        """get_main_task"""
        parser = Parser(self.webdriver.page_source)
        main_tasks = parser.get_tasks_from_main()

    def get_smart_list(self):
        smart_view_area = self.webdriver.driver.find_element_by_id('smart-project-view-area')

