from driver import Driver
from parser import Parser
import json
#test
def print_section(section):
    section_title = section[0]
    section_tasks = section[1]
    print(section_title)
    for task in section_tasks:
        print('    '+task.title)
        for sub in task.subtasks:
            print('        '+sub.text)


if __name__ == '__main__':
    driver = Driver(debug=True)
    driver.init_main()
    if driver.status == 'main':
        parser = Parser(driver.get_page_source())
        main_tasks = parser.get_tasks_from_main()






