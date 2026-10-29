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
