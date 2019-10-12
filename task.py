class Task:
    def __init__(self, text: str, checkable: bool):
        self.text = text
        self.checkable = checkable
        self.completed = None

    def set_completed(self, completed: bool):
        if self.checkable:
            self.completed = completed

    def get_completed(self):
        if self.checkable:
            return self.completed
        return None


class TickTask:
    def __init__(self, title: str):
        self.title = title
        self.subtasks = []

    def add_subtask(self, task: Task):
        self.subtasks.append(task)


class TickSection:
    def __init__(self, section: str):
        self.section = section
        self.tasks = []

    def add_task(self, task: TickTask):
        self.tasks.append(task)






