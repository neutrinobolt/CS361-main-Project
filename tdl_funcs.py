"""Function library for Dewitt."""

import json
from datetime import date as dt
import tkinter as tk
from task_class import Task


###################################################################################################
#Main Window Functions
###################################################################################################
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

def update_day_tasks(od_frame: tk.Frame,
                     td_frame: tk.Frame,
                     task_list: list[Task],
                     od_tasks: list[Task],
                     td_tasks: list[Task],
                     current_date: dt,
                     user: dict,
                     tm_frame: tk.Frame
                     ):
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
    pack_tasks(od_tasks,
               od_list,
               tm_frame,
               od_frame,
               td_frame,
               od_tasks,
               td_tasks,
               current_date,
               user,
               "",
               task_list)
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
    pack_tasks(td_tasks,
               td_list,
               tm_frame,
               od_frame,
               td_frame,
               od_tasks,
               td_tasks,
               current_date,
               user,
               "",
               task_list)
    td_display.pack()
    td_header.pack()
    td_list.pack()



def mark_done(task_list: list[Task],
              task_id: int,
              od_frame: tk.Frame,
              td_frame: tk.Frame,
              od_tasks: list[Task],
              td_tasks: list[Task],
              current_date: dt,
              user: dict,
              tm_frame: tk.Frame):
    """Set completion status of task with id (task_id) to complete,
    update page """
    get_task_by_id(task_list, task_id).completed = True
    update_day_tasks(od_frame,
                     td_frame,
                     task_list,
                     od_tasks,
                     td_tasks,
                     current_date,
                     user,
                     tm_frame)

def pack_tasks(ptasks:list[Task],
               root:tk.Frame,
               tm_frame: tk.Frame,
               od_frame: tk.Frame,
               td_frame: tk.Frame,
               od_tasks: list[Task],
               td_tasks: list[Task],
               current_date: dt,
               user: dict,
               error_msg: str,
               all_tasks: list[Task]):
    """Take alll tasks in a list and pack them in a frame with
    a mark-done button and an edit button."""
    for ptask in ptasks:
        task_frame = tk.Frame(root)
        task_id = ptask.t_id
        finish_btn = tk.Button(task_frame, text="Mark Done",
                               command=lambda:mark_done(all_tasks,
                                                        task_id,
                                                        od_frame,
                                                        td_frame,
                                                        od_tasks,
                                                        td_tasks,
                                                        current_date,
                                                        user,
                                                        tm_frame))
        task_text = tk.Label(task_frame, text=ptask.title)
        edit_btn = tk.Button(task_frame, text="Edit Task",
                             command=lambda: task_edit(tm_frame,
                                               ptask,
                                               all_tasks,
                                               user,
                                               current_date,
                                               od_frame,
                                               td_frame,
                                               od_tasks,
                                               td_tasks,
                                               error_msg))
        finish_btn.grid(row=0, column=0)
        task_text.grid(row=0, column=1)
        edit_btn.grid(row=0, column=2)
        task_frame.pack()

def end_prgm(u_tasks: list[Task],
             od_tasks: list[Task],
             td_tasks: list[Task],
             user: dict,
             window: tk.Tk):
    """
    -Update json file with current task data
    -end all side programs (once applicapble)
    -close window."""
    #Update json file
    #replaced changed tasks
    changed_tasks:list[Task] = od_tasks + td_tasks
    for old_task in u_tasks:
        for new_task in changed_tasks:
            if new_task.t_id == old_task.t_id:
                old_task = new_task

    #Convert task list to json readable dict
    task_list_dict: list[dict] = []
    for in_task in u_tasks:
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
                "uname": user["uname"], #change later
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

###################################################################################################
#Task Maker Window Functions
###################################################################################################

def subtask_disconnect(parent: Task, sub: Task):
    """Remove subtask from parent's subtask list, set subtask's parent to None"""
    parent.t_subs.remove(sub.t_id)
    sub.t_parent = None

def ditch_sub(parent:Task, sub:Task, out_frame: tk.Frame, task_list: list[Task]):
    """disconnect subtasks, rerun list_subs"""
    subtask_disconnect(parent, sub)
    list_subs(parent, out_frame, task_list)

def list_subs(parent_task: Task, out_frame: tk.Frame, task_list: list[Task]):
    """Clear out_frame, then Pack all subtasks of parent_task to outframe. For each subtask, diplay:
    - Subtask name
    - Remove Subtask button"""
    print(f"Showing subtasks for parent task id {parent_task.t_id}")
    for sub_id in parent_task.t_subs:
        print(f"retreiving data for subtask id {sub_id}")
        subtask = get_task_by_id(task_list, sub_id)
        sub_frame = tk.Frame(out_frame)
        sub_title = tk.Label(sub_frame, text=subtask.title)
        sub_remover = tk.Button(sub_frame, text="Remove from subtask list",
                                command=lambda: ditch_sub(parent_task,
                                                          subtask,
                                                          out_frame,
                                                          task_list))
        sub_title.grid(row=0, column=0)
        sub_remover.grid(row=0, column=1)
        sub_frame.pack()

def return_no_parent(in_task: Task,
                     p_list_frame: tk.Frame,
                     task_list: list[Task],
                     window: tk.Frame,
                     grid_to_col: int,
                     user: dict,
                     current_date: dt,
                     od_frame: tk.Frame,
                     td_frame: tk.Frame,
                     od_tasks: list[Task],
                     td_tasks: list[Task]):
    """Set input task parent to none, destroy p list, update editor"""
    subtask_disconnect(get_task_by_id(task_list, in_task.t_parent), in_task)
    p_list_frame.destroy()
    update_tmaker(window,
                  grid_to_col,
                  in_task,
                  task_list,
                  user,
                  current_date,
                  od_frame,
                  td_frame,
                  od_tasks,
                  td_tasks,
                  error_msg= ""
                  )

def return_parent(in_sub: Task,
                  in_parent: Task,
                  p_list_frame: tk.Frame,
                  window: tk.Frame,
                  grid_to_col: int,
                  u_tasks: list[Task],
                  user:dict,
                  current_date:dt,
                  od_frame: tk.Frame,
                  td_frame: tk.Frame,
                  od_tasks: list[Task],
                  td_tasks: list[Task]
                  ):
    """Set input subtask to input parent, add subtask to parent's sub list,
    destroy plist frame, update editor"""
    in_sub.t_parent = in_parent.t_id
    if in_sub.t_id not in in_parent.t_subs:
        in_parent.t_subs.append(in_sub.t_id)
    p_list_frame.destroy()
    update_tmaker(window,
                  grid_to_col,
                  in_sub,
                  u_tasks,
                  user,
                  current_date,
                  od_frame,
                  td_frame,
                  od_tasks,
                  td_tasks,
                  error_msg="")

def show_p_list(task_list:list[Task],
                parent_col: int,
                in_task: Task,
                window: tk.Frame,
                user: dict,
                current_date: dt,
                od_frame: tk.Frame,
                td_frame: tk.Frame,
                od_tasks: list[Task],
                td_tasks: list[Task]):
    """Display a list of all incomplete tasks as buttons, and one 'select none' button.
    - Buttons will return input task as parent to input task."""
    p_list_frame = tk.Frame(window)
    return_none = tk.Button(p_list_frame,
                            text="None",
                            command=lambda:return_no_parent(in_task,
                                                            p_list_frame,
                                                            task_list,
                                                            window,
                                                            parent_col,
                                                            user,
                                                            current_date,
                                                            od_frame,
                                                            td_frame,
                                                            od_tasks,
                                                            td_tasks))
    return_none.pack()
    unfinished_tasks = []
    for task in task_list:
        if not task.completed:
            unfinished_tasks.append(task)
    for unfinished in unfinished_tasks:
        task_btn = tk.Button(p_list_frame,
                             text=unfinished.title,
                             command=lambda: return_parent(in_task,
                                                           unfinished,
                                                           p_list_frame,
                                                           window,
                                                           parent_col,
                                                           task_list,
                                                           user,
                                                           current_date,
                                                           od_frame,
                                                           td_frame,
                                                           od_tasks,
                                                           td_tasks))
        task_btn.pack()
    p_list_frame.grid(row=0,column=parent_col + 1)

def return_no_subtask(s_list_frame: tk.Frame):
    """Make no change. Destroy s_list frame."""
    s_list_frame.destroy()

def show_s_list(task_list:list[Task],
                parent_col: int,
                in_task: Task,
                window: tk.Frame,
                user: dict,
                current_date: dt,
                od_frame: tk.Frame,
                td_frame: tk.Frame,
                od_tasks: list[Task],
                td_tasks: list[Task]):
    """Display a list of all unfinished tasks as buttons, and one 'select none' button.
    - buttons will close list and return input task as subtask to input task."""
    s_list_frame = tk.Frame(window)
    return_none = tk.Button(s_list_frame,
                                text="None",
                                command=lambda:return_no_subtask(s_list_frame))
    return_none.pack()
    unfinished_tasks = []
    for task in task_list:
        if not task.completed:
            unfinished_tasks.append(task)
    for unfinished in unfinished_tasks:
        task_btn = tk.Button(s_list_frame,
                                text=unfinished.title,
                                command=lambda: return_parent(unfinished,
                                                            in_task,
                                                            s_list_frame,
                                                            window,
                                                            parent_col,
                                                            task_list,
                                                            user,
                                                            current_date,
                                                            od_frame,
                                                            td_frame,
                                                            od_tasks,
                                                            td_tasks))
        task_btn.pack()
    s_list_frame.grid(row=0,column=parent_col + 1)

def input_validate(check_day: str,
                   check_month: str,
                   check_year: str,
                   check_priority: str) -> tuple:
    """Validate input info.
    Make sure input day, month, year, and priority are all ints,
    that input date is valid,
    and input priority is in acceptable range."""
    input_valid = True
    error_msg = ""

    try:
        int(check_day)
    except TypeError:
        input_valid = False
        error_msg = "ERROR: day must be a number."

    try:
        int(check_month)
    except TypeError:
        input_valid = False
        error_msg = "ERROR: month must be a number."

    try:
        int(check_year)
    except TypeError:
        input_valid = False
        error_msg = "ERROR: year must be a number."

    try:
        int(check_priority)
    except TypeError:
        input_valid = False
        error_msg = "ERROR: priority must be a number."

    try:
        dt(int(check_year), int(check_month), int(check_day))
    except TypeError:
        input_valid = False
        error_msg = "ERROR: Must input a valid date."

    if int(check_priority) not in range(0, 11):
        input_valid = False
        error_msg = "ERROR: Priority must be between 0 and 10."

    return (input_valid, error_msg)

def save_task(task_list: list[Task],
              task_id: int,
              in_task: Task,
              new_title: str,
              new_day: str,
              new_month: str,
              new_year: str,
              new_priority: str,
              user: dict,
              task_frame: tk.Frame,
              # arguments for updating to-do
              od_frame: tk.Frame,
              td_frame: tk.Frame,
              od_tasks: list[Task],
              td_tasks: list[Task],
              current_date: dt,
              tm_frame: tk.Frame,
              # args for updating tmaker
              grid_to_col:int
              ):
    """
    - Validate editor data. If valid input:
    - Check if task of input id already exists. If so: 
    - Replace task. If not: 
    - Create new task
    - Add new task to task list
    - update user task count
    - Close Editor window
    - Update main to-do list"""
    #Validate Data
    validation= input_validate(new_day, new_month, new_year, new_priority)
    if not validation[0]:
        update_tmaker(task_frame,
                      grid_to_col,
                      in_task,
                      task_list,
                      user,
                      current_date,
                      od_frame,
                      td_frame,
                      od_tasks,
                      td_tasks,
                      error_msg=validation[1])
    else:
        #Create new task from input
        in_task.title = new_title
        in_task.due = dt(int(new_year), int(new_month), int(new_day))
        in_task.priority = int(new_priority)
        #Check for task matching id
        task_exists = False
        for check_task in task_list:
            if check_task.t_id == task_id:
                #replace check_task with task
                check_task = in_task
                task_exists = True
        if not task_exists:
            task_list.append(in_task)
            #Update user task count
            user["task_count"] += 1

        #Close editor window
        task_frame.destroy()

        #Update to-do
        update_day_tasks(od_frame,
                         td_frame,
                         task_list,
                         od_tasks,
                         td_tasks,
                         current_date,
                         user,
                         tm_frame)

def task_delete(task_list: list[Task],
                dead_task: Task,
                editor_frame: tk.Frame,
                od_frame: tk.Frame,
                td_frame: tk.Frame,
                od_tasks: list[Task],
                td_tasks: list[Task],
                current_date: dt,
                user: dict
                ):
    """Completely remove task from task list. Update windows."""
    task_list.remove(get_task_by_id(task_list, dead_task.t_id))
    editor_frame.destroy()
    update_day_tasks(od_frame,
                     td_frame,
                     task_list,
                     od_tasks,
                     td_tasks,
                     current_date,
                     user,
                     editor_frame)


def update_tmaker (window: tk.Frame,
                   grid_to_col: int,
                   in_task: Task,
                   u_tasks: list[Task],
                   user: dict,
                   current_date: dt,
                   od_frame: tk.Frame,
                   td_frame: tk.Frame,
                   od_tasks: list[Task],
                   td_tasks: list[Task],
                   error_msg: str):
    """Fill in tmaker frame, grid to window."""

    #Fill in frame
    tm_frame = tk.Frame(window)
    #Header
    tm_head = tk.Frame(tm_frame)
    tm_title = tk.Label(tm_head)
    if grid_to_col > 0:
        tm_title.configure(text="Subtask Details")
    else:
        tm_title.configure(text="Task Details")
    tm_errors = tk.Label(tm_head, text=error_msg)
    tm_errors.pack()
    tm_head.pack()
    tm_title.pack()

    #Build Title block
    task_title = tk.Frame(tm_frame)
    title_label = tk.Label(task_title, text="Task Name",font=('calibre',10, 'bold'))
    title_var = tk.StringVar()
    title_entry = tk.Entry(task_title,
                           textvariable= title_var,
                           font=('calibre',10, 'normal'))
    title_var.set(in_task.title)
    title_label.grid(row=0, column=0)
    title_entry.grid(row=0, column=1)
    task_title.pack()

    #Build Date block
    task_date = tk.Frame(tm_frame)
    date_title = tk.Label (task_date, text="Due Date")
    d_frame = tk.Frame(tm_frame)
    month_var = tk.StringVar()
    day_var = tk.StringVar()
    year_var = tk.StringVar()
    month_entry = tk.Entry(d_frame, textvariable=month_var)
    day_entry = tk.Entry(d_frame, textvariable=day_var)
    year_entry = tk.Entry(d_frame, textvariable=year_var)
    month_label = tk.Label(d_frame, text="month", font=('calibre',10, 'bold'))
    day_label = tk.Label(d_frame, text="day", font=('calibre',10, 'bold'))
    year_label = tk.Label(d_frame, text="year", font=('calibre',10, 'bold'))
    month_var.set(in_task.due.month)
    day_var.set(in_task.due.day)
    year_var.set(in_task.due.year)
    month_entry.grid(row=0, column=0)
    day_entry.grid(row=0, column=1)
    year_entry.grid(row=0, column=2)
    month_label.grid(row=1, column=0)
    day_label.grid(row=1, column=1)
    year_label.grid(row=1, column=2)

    date_title.pack()
    d_frame.pack()
    task_date.pack()

    #Build Parent Task block
    parent_frame = tk.Frame(tm_frame)
    parent_label = tk.Label(parent_frame)
    if in_task.t_parent is None:
        parent_label.configure(text="No Parent task attached.")
    else:
        parent_label.configure(text=f"Parent Task: {get_task_by_id(u_tasks,
                                                                   in_task.t_parent)}")
    parent_picker = tk.Button(parent_frame, text="Choose parent task",
                              command= lambda:show_p_list(u_tasks,
                                                          grid_to_col,
                                                          in_task,
                                                          window,
                                                          user,
                                                          current_date,
                                                          od_frame,
                                                          td_frame,
                                                          od_tasks,
                                                          td_tasks))
    parent_label.pack()
    parent_picker.pack()
    parent_frame.pack()

    #Build subtask block
    sub_frame = tk.Frame(tm_frame)
    sub_title = tk.Label(sub_frame, text=f"Subtasks ({len(in_task.t_subs)})")
    sub_list = tk.Frame(sub_frame)
    list_subs(in_task, sub_list, u_tasks)
    add_sub_btn = tk.Button(sub_frame, text="Add Subtask",
                            command=lambda:show_s_list(u_tasks,
                                                       grid_to_col,
                                                       in_task,
                                                       window,
                                                       user,
                                                       current_date,
                                                       od_frame,
                                                       td_frame,
                                                       od_tasks,
                                                       td_tasks))
    sub_title.pack()
    sub_list.pack()
    add_sub_btn.pack()
    sub_frame.pack()

    #Build Priority block
    priority_frame = tk.Frame(tm_frame)
    priority_title = tk.Label(priority_frame, text="Priority Level (0-10, 0 is highest priority)")
    priority_var = tk.StringVar()
    priority_entry = tk.Entry(priority_frame,
                              textvariable=priority_var,
                              font=('calibre',10, 'bold'))
    priority_var.set(in_task.priority)
    priority_title.pack()
    priority_entry.pack()
    priority_frame.pack()

    #Build Create Subtask button
    new_sub_btn = tk.Button(tm_frame,
                            text="Create New Subtask",
                            command=lambda: update_tmaker(window,
                                                          grid_to_col + 1,
                                                          Task(t_id=user["task_count"] + 1,
                                                               title= "",
                                                               due=current_date,
                                                               tsubs=[],
                                                               priority=10,
                                                               completed=False
                                                               ),
                                                               u_tasks,
                                                               user,
                                                               current_date,
                                                               od_frame,
                                                               td_frame,
                                                               od_tasks,
                                                               td_tasks,
                                                               error_msg
                                                               ))
    new_sub_btn.pack()

    #Build Save Task button
    save_btn = tk.Button(tm_frame, text="Save Task",
                         command=lambda: save_task(u_tasks,
                                                   in_task.t_id,
                                                   in_task,
                                                   title_var.get(),
                                                   day_var.get(),
                                                   month_var.get(),
                                                   year_var.get(),
                                                   priority_var.get(),
                                                   user,
                                                   tm_frame,
                                                   od_frame,
                                                   td_frame,
                                                   od_tasks,
                                                   td_tasks,
                                                   current_date,
                                                   window,
                                                   grid_to_col
                                                   ))
    save_btn.pack()

    #Build Quit w/o saving button
    task_delete_btn = tk.Button(tm_frame,
                                text="Exit Without Saving (Delete Task)",
                                command=lambda: task_delete(u_tasks,
                                                            in_task,
                                                            tm_frame,
                                                            od_frame,
                                                            td_frame,
                                                            od_tasks,
                                                            td_tasks,
                                                            current_date,
                                                            user))
    task_delete_btn.pack()

    #grid to window
    tm_frame.grid(row=0, column=grid_to_col)

def task_edit(window: tk.Frame,
              in_task:Task,
              u_tasks: list[Task],
              user: dict,
              current_date: dt,
              od_frame: tk.Frame,
              td_frame: tk.Frame,
              od_tasks: list[Task],
              td_tasks: list[Task],
              error_msg:str):
    """Run update_tmaker, displaying input task."""
    update_tmaker(window,
                  0,
                  in_task,
                  u_tasks,
                  user,
                  current_date,
                  od_frame,
                  td_frame,
                  od_tasks,
                  td_tasks,
                  error_msg)

def task_create(window: tk.Frame,
                u_tasks: list[Task],
                user: dict,
                current_date: dt,
                od_frame: tk.Frame,
                td_frame: tk.Frame,
                od_tasks: list[Task],
                td_tasks: list[Task],
                error_msg:str):
    """Create blank task and display with update_tmaker"""
    in_task = Task(t_id=user["task_count"] + 1,
                        title= "",
                        due=current_date,
                        tsubs=[],
                        priority=10,
                        completed=False)
    update_tmaker(window,
                  0,
                  in_task,
                  u_tasks,
                  user,
                  current_date,
                  od_frame,
                  td_frame,
                  od_tasks,
                  td_tasks,
                  error_msg)
