"""Main running file for Dewitt: branching to-do list in Python Tkinter.
This file is to be run to use the full app. 
It contains code for running the main page of the app which contains:
- Title "To-Do Today
- Button "Create New Task"
- Overdue Task List containing:
    - Title stating how many overdue tasks there are
    - list of overdue tasks, each showing:
    - Button to mark task done
    - task name
    - Button to edit task
- Task list Due Today containing similar items to Overdue list
- Close Button
"""

import json
from pprint import pprint
import tkinter as tk
from datetime import date as dt
from task_class import Task

USER_CHECK = "test" #replace with login function when created

current_date = dt.today()
current_day = current_date.day
current_month = current_date.month
current_year = current_date.year

task_data = {}
tasks:list[Task] = []
user = {}

od_tasks:list[Task] = []
td_tasks:list[Task] = []


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

def get_task_by_id (task_list: list[Task], task_id: int) -> Task:
    """Given a list of tasks, search list for task with matching id, return task"""
    for l_task in task_list:
        if l_task.t_id == task_id:
            return l_task
    return None

def task_edit(task:Task):
    pass

def task_create():
    pass

def toggle_frame(od_frame: tk.Frame,
                   user_in: dict,
                   in_btn: tk.Button = None):
    """Hide or show frame with button."""
    user_in["show_overdue"] = not user_in["show_overdue"]
    if user_in["show_overdue"]:
        od_frame.pack()
        in_btn.configure(text="hide")
    else:
        od_frame.pack_forget()
        in_btn.configure(text="show")

def update_day_tasks(od_frame: tk.Frame, td_frame: tk.Frame, task_list: list[Task]):
    """Update day display with current contents of tasks list.
    - Clear current overdue and today sections
    - fill in with current overdue and today sections
    """
    #Clear frames
    for od_object in od_frame.winfo_children():
        od_object.destroy()
    for td_object in td_frame.winfo_children():
        td_object.destroy()

    od_tasks.clear()
    #Fill in Overdue Frame
    for od_check_task in task_list:
        #Create datetime object from due date
        if od_check_task.due < current_date and not od_check_task.completed:
            od_tasks.append(od_check_task)
    od_header = tk.Frame(od_frame)
    od_display = tk.Label(od_header, text=f"{len(od_tasks)} unfinished tasks overdue.")
    od_list = tk.Frame(od_frame)
    od_toggle = tk.Button(od_header, text="Hide",
                        command= None)
    od_toggle.configure(command= lambda: toggle_frame(od_list, user, od_toggle))
    pack_tasks(od_tasks, od_list, od_frame, td_frame)
    od_display.grid(row=0, column=1)
    od_toggle.grid(row=0, column=2)
    od_header.pack()
    od_list.pack()

    #fill in td frame
    td_tasks.clear()
    for td_check_task in task_list:
        if td_check_task.due == current_date and not td_check_task.completed:
            td_tasks.append(td_check_task)
    td_header = tk.Frame(td_frame)
    td_display = tk.Label(td_header, text=f"{len(td_tasks)} tasks due today.")
    td_list = tk.Frame(td_frame)
    pack_tasks(td_tasks, td_list, od_frame, td_frame)
    td_display.pack()
    td_header.pack()
    td_list.pack()



def mark_done(task_list: list[Task], task_id: int, od_frame: tk.Frame, td_frame: tk.Frame):
    """Set completion status of task with id (task_id) to complete,
    update page """
    get_task_by_id(task_list, task_id).completed = True
    update_day_tasks(od_frame, td_frame, task_list)

def pack_tasks(ptasks:list[Task], root:tk.Frame, od_frame: tk.Frame, td_frame: tk.Frame):
    """Take alll tasks in a list and pack them in a frame with
    a mark-done button and an edit button."""
    for ptask in ptasks:
        task_frame = tk.Frame(root)
        finish_btn = tk.Button(task_frame, text="Mark Done",
                               command=lambda:mark_done(tasks, ptask.t_id, od_frame, td_frame))
        task_text = tk.Label(task_frame, text=ptask.title)
        edit_btn = tk.Button(task_frame, text="Edit Task",
                             command=task_edit(ptask))
        finish_btn.grid(row=0, column=0)
        task_text.grid(row=0, column=1)
        edit_btn.grid(row=0, column=2)
        task_frame.pack()

def end_prgm():
    """
    -Update json file with current task data
    -end all side programs (once applicapble)
    -close window."""
    #Update json file
    #replaced changed tasks
    changed_tasks:list[Task] = od_tasks + td_tasks
    for old_task in tasks:
        for new_task in changed_tasks:
            if new_task.t_id == old_task.t_id:
                old_task = new_task

    #Convert task list to json readable dict
    task_list_dict: list[dict] = []
    for in_task in tasks:
        task_dict = {
            "id": in_task.t_id,
            "title": in_task.title,
            "dday": in_task.due.day,
            "dmonth": in_task.due.month,
            "dyear": in_task.due.year,
            "parent": in_task.t_parent,
            "subtasks": in_task.t_subs,
            "priority": in_task.priority,
            "completed": in_task.completed}
        task_list_dict.append(task_dict)
    full_json = {
        "users": [
            {
                "uname": USER_CHECK, #change late
                "task_count": len(task_list_dict),
                "show_overdue": user["show_overdue"],
                "tasks": task_list_dict
            }
        ]
    }

    json_tasks = json.dumps(full_json, indent=4)
    #write to json file
    with open("tasks.json", mode="w", encoding="utf-8") as outfile:
        outfile.write(json_tasks)

    #Close window
    window.destroy()

#get json string
with open("./tasks.json", mode="r", encoding="utf-8") as tfile:
    tdata_json = tfile.read()
    task_data = json.loads(tdata_json)

#Get user task data
usernames = []
for user in task_data["users"]:
    if user["uname"] == USER_CHECK:
        ind = task_data["users"].index(user)
        user = task_data["users"][ind]
        tasks_dict = task_data["users"][ind]["tasks"]
        tasks = taskify(tasks_dict)


window = tk.Tk()
window.title("Dewitt")

################################################################
#main page display, initial setup
################################################################
p_main = tk.Frame(window)

#Header
header = tk.Frame(p_main)
title = tk.Label(header, text="To-Do Today")
task_creator = tk.Button(header,
                         text="Create New Task",
                         command= task_create)
title.pack()
task_creator.pack()

header.pack()


overdue = tk.Frame(p_main)
today = tk.Frame(p_main)

update_day_tasks(overdue, today, tasks)

overdue.pack()
today.pack()

quit_btn = tk.Button(p_main,text="Close Dewitt",
                     command=end_prgm)
quit_btn.pack()

p_main.pack()

window.mainloop()
