"""Defines task Data Structure."""

from datetime import date as dt

class Task:
    """ Task object for storing and tracking task data. contains:
    - Task id (int)
    - Task Title (str)
    - Task Due Date (dt.Date)
    - Parent Task (Task or Null)
    - Subtasks (List of Tasks)
    - Priority lvl (int 0-10)
    """
    def __init__(self,
                 t_id:int,
                 title:str,
                 due:dt,
                 tsubs: list[int],
                 priority:int,
                 completed:bool,
                 tparent: int = None
                 ):
        self.t_id = t_id
        self.title = title
        self.due = due
        self.t_parent = tparent
        self.t_subs = tsubs
        self.priority = priority
        self.completed = completed

def get_overdue(task_list: list[Task],
                today: dt) ->list[Task]:
    """Return a list of all tasks in input task list
    that are incomplete and overdue."""
    out_list = []
    for task in task_list:
        if not task.completed and task.due < today:
            out_list.append(task)
    return out_list

def get_today(task_list: list[Task],
                today: dt) -> list[Task]:
    """Return a list of all tasks in input task list
    that are incomplete and due today."""
    out_list = []
    for task in task_list:
        if not task.completed and task.due == today:
            out_list.append(task)
    return out_list

def get_task_by_id (task_list: list[Task], task_id: int) -> Task:
    """Given a list of tasks, search list for task with matching id, return task"""
    for l_task in task_list:
        if l_task.t_id == task_id:
            return l_task
    return None

def taskify(in_list: list[dict])->list[Task]:
    """Take an input list of task dictionaries and output
    a list of task objects"""
    out_list = []
    for in_task in in_list:
        out_task = Task(in_task["id"],
                        in_task["title"],
                        dt(in_task["dyear"],
                           in_task["dmonth"],
                           in_task["dday"]),
                        in_task["subtasks"],
                        in_task["priority"],
                        in_task["completed"],
                        in_task["parent"])
        out_list.append(out_task)
    return out_list
