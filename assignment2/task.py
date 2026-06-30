import os

class Task(object):
    def __init__(self, task_path):
        self.task_path = os.path.abspath(task_path)
        self.task_name = os.path.basename(task_path)

        self.__dict__.update(self._build_lookup())
        

    def _build_lookup(self):
        return {
            "task_name": self.task_name,
            "task_path": self.task_path,
            "instruction": os.path.join(self.task_path, "instruction.md"),
            "dockerfile": os.path.join(self.task_path, "dockerfile"),
            "enviroment_dir": os.path.join(self.task_path, "environment"),
        }

    # def get_instruction(self, task)

    