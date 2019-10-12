from bs4 import BeautifulSoup
from task import Task, TickTask

class Parser:
    def __init__(self, html):
        self.soup = BeautifulSoup(html, 'html.parser')

    def get_section_from_main(self):
        return self.soup.findAll('section', {'class':'section opened'})

    def get_task_from_section(self, section):
        ttasks = []
        for task in section.findAll('li'):
            title = task.find('div', {'class':'title'}).text
            ttask = TickTask(title=title)
            subtask = task.find('div', {'class': 't-subtask'}).findAll('div')
            for sub in subtask:
                ttask.add_subtask(self.get_subtask_from_task(sub))
            ttasks.append(ttask)
        return ttasks

    def get_subtask_from_task(self, subtask):
        text = subtask.text
        completed = subtask.attrs['class']
        completed = True if completed == 'completed' else False
        checkable = subtask.find('span').attrs['class']
        checkable = True if checkable == 'checker' else False
        task = Task(text=text, checkable=checkable)
        task.set_completed(completed)
        return task

    def get_tasks_from_main(self):
        main_sections = self.get_section_from_main()
        main_tasks = {}
        for section in main_sections:
            section_title = section.find('div', {'class':'section-header open'}).text
            main_tasks[section_title] = self.get_task_from_section(section)
        return main_tasks 
