class Task:
    def __init__(self, text, checkable):
        self.text = text
        self.checkable = checkable
        self.completed = None

    def set_completed(self, completed):
        if self.checkable:
            self.completed = completed

    def get_completed(self):
        if self.checkable:
            return self.completed
        return None


class TickTask():
    def __init__(self, title):
        self.title = title
        self.subtasks = []

    def add_subtask(self, task):
        self.subtasks.append(task)





