"""Contains object class for the daily to-do list and subclass for task displays."""

import json
from datetime import date as dt
import tkinter as tk
import task_class as tc
from task_editor import TaskEdit

class TaskDisp:
    """TaskDisp contains info regardig:
    - parent display frame (input)
    - input task id (input)
    - user task list (input)
    - editor object (input)
    - Mark Done Button
    - Task Title label
    - Task Edit Button
    - Functions:
        - Mark Done
        - Edit task
    """
    def __init__(self,
                 parent_frame: tk.Frame,
                 task_id: int,
                 u_tasks: list[tc.Task],
                 editor: TaskEdit):
        """Create frame within parent frame, fill with three items in a row"""
        self.disp_frame = tk.Frame(parent_frame)
        self.task = tc.get_task_by_id(u_tasks, task_id)
        self.mark_done_btn = tk.Button(self.disp_frame,
                                       text="Mark Done",
                                       command=lambda:self.mark_done(u_tasks))
        self.mark_done_btn.grid(row=0, column=0)
        self.title = tk.Label(self.disp_frame,
                              text=self.task.title)
        self.title.grid(row=0, column=1)
        self.edit_btn = tk.Button(self.disp_frame,
                                  text="Edit",
                                  command=lambda:self.task_edit(editor,
                                                                tc.get_task_by_id(u_tasks,
                                                                                  task_id)))
        self.edit_btn.grid(row=0, column=2)

    def mark_done(self, u_tasks:list[tc.Task]):
        """Set task complete to true, remove task from list"""
        self.task.completed = True
        #replace original task
        for task in u_tasks:
            if task.t_id == self.task.t_id:
                task = self.task
                print("Updated original task id")
        #Remove task display from parent
        self.disp_frame.destroy()

    def task_edit(self, editor: TaskEdit, in_task: tc.Task):
        """Configure input editor with details from input task, pack editor to frame"""
        #Configure editor frame
        editor.task_id = in_task.tid
        editor.title_var.set(in_task.title)
        editor.month_var.set(in_task.due.month)
        editor.day_var.set(in_task.due.day)
        editor.year_var.set(in_task.due.year)
        editor.priority_var.set(in_task.priority)
        editor.show_parent(in_task)
        editor.show_subs(in_task)

        #Pack Editor
        editor.e_frame.pack()

class Daylist:
    """Daylist contains info regarding:
            - Parent Frame
            - All frames within Parent, including:
                - Header
                - Overdue Task List
                - Today's Task List
                - Close Window Button
            - Associated editor object
            - Current date
            - Current User dict
            - Full task list
            - Functions:
                - Update daylist frame
                - Get overdue tasks
                - hide/show overdue list
                - Get today's tasks
                - Display task list in a frame
                - mark task done
                - create new task
                - edit existing task"""

    def __init__(self,
                 window: tk.Tk,
                 root: tk.Frame,
                 user_check: str,
                 today: dt,
                 t_editor: TaskEdit = None
                 ):
        """Using input arguments, create remaining data"""
        #Set input values
        self.window = window
        self.root = root
        self.u_dict = {}
        self.t_editor = t_editor
        self.today = today
        self.task_data = {}
        self.tasks = []
        self.user_check = user_check

        #get json string
        with open("./tasks.json", mode="r", encoding="utf-8") as tfile:
            tdata_json = tfile.read()
            self.task_data = json.loads(tdata_json)

        #Get user task data
        for check_user in self.task_data["users"]:
            if check_user["uname"] == user_check:
                tasks_dict = check_user["tasks"]
                self.u_dict = check_user
                self.tasks = tc.taskify(tasks_dict)

        #derive remaining values
        #Header
        self.header = tk.Frame(self.root)
        self.h_title = tk.Label(self.header, text="To-Do Today")
        self.h_title.pack()
        self.task_creator = tk.Button(self.header,
                                      text="Create New Task",
                                      command= self.task_create)
        self.task_creator.pack()

        self.header.pack()

        #Overdue Tasks
        self.od_tasks: list[tc.Task] = []
        self.od_frame = tk.Frame(self.root)
        self.od_head = tk.Frame(self.od_frame)
        self.od_title = tk.Label(self.od_head)
        self.od_title.grid(row=0, column=0)
        self.od_toggle = tk.Button(self.od_head,
                                   text="hide",
                                   command=self.hide_overdue)
        if not self.u_dict["show_overdue"]:
            self.od_toggle.configure(text="show",
                                     command=self.show_overdue)
        self.od_toggle.grid(row=0, column=1)
        self.od_head.pack()

        self.od_list = tk.Frame(self.od_frame)
        self.od_disps: list[TaskDisp] = []

        self.od_frame.pack()


        #Today Tasks
        self.td_tasks: list[tc.Task] = []
        self.td_frame = tk.Frame(self.root)

        self.td_head = tk.Frame(self.td_frame)
        self.td_title = tk.Label(self.td_head)
        self.td_title.pack()
        self.td_head.pack()
        self.td_list = tk.Frame(self.td_frame)
        self.td_disps: list[TaskDisp] = []

        self.td_frame.pack()

        #Save Button
        self.save_btn = tk.Button(self.root,
                                  text="Save task",
                                  command= self.save_task)

        #Close Button
        self.quit_btn = tk.Button(self.root,
                                  text="Close Dewitt",
                                  command= self.end_prgm)
        self.quit_btn.pack()


    def input_validate(self,
                        check_day: str,
                        check_month: str,
                        check_year: str,
                        check_priority: str) -> tuple[bool, str]:
        """Check if input entry values are valid.
        Valid conditions are only met if:
        - day, month, year and priority fields all hold strings that can be converted to ints
        - day, month, and year fields can be combined to create a valid date
        - priority entry is between 0 and 10 (inclusive)
        Function returns a tuple containing valid status (true if valid) and error message
        (empty string if valid)"""

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
    
    
    def save_task(self):
        """After validating input, either return an error message or:
        - create a new task from input fields and current set id
        - add new task to main window task list
        - update main window
        - hide editor window"""
        if self.t_editor is not None:
            #Get entry values
            in_month = self.t_editor.month_var.get()
            in_day = self.t_editor.day_var.get()
            in_year = self.t_editor.year_var.get()
            in_priority = self.t_editor.priority_var.get()

            input_valid = self.input_validate(in_day, in_month, in_year, in_priority)

            if input_valid[0]:
                self.t_editor.errors.pack_forget()

                #Create new task from input
                new_task = tc.Task(self.t_editor.task_id,
                                    self.t_editor.title_var.get(),
                                    dt(int(in_year), int(in_month), int(in_day)),
                                    self.t_editor.subs,
                                    int(in_priority),
                                    False,
                                    self.t_editor.t_parent
                                    )
                self.tasks.append(new_task)
                #Hide editor frame
                self.t_editor.e_frame.pack_forget()
                self.save_btn.pack_forget()
                self.header.pack()
                self.od_frame.pack()
                self.td_frame.pack()
                self.quit_btn.pack()
                self.update()

            else:
                self.t_editor.errors.configure(text=input_valid[1])
                self.t_editor.errors.pack()

    def task_create(self):
        """Open Task Creator menu with date input reflecting current date,
        all other fields empty."""

        if self.t_editor is not None:
            #set fields
            self.t_editor.title_var.set("")
            self.t_editor.month_var.set(self.today.month)
            self.t_editor.day_var.set(self.today.day)
            self.t_editor.year_var.set(self.today.year)
            self.t_editor.priority_var.set(0)

            self.t_editor.task_id = self.u_dict["task_count"] + 1

            self.t_editor.e_frame.grid(row=0, column=self.t_editor.grid_to_col)

            self.header.pack_forget()
            self.od_frame.pack_forget()
            self.td_frame.pack_forget()
            self.quit_btn.pack_forget()

            self.save_btn.pack()

    def hide_overdue(self):
        """Unpack overdue list, set user show_overdue to false, change button"""
        self.od_list.pack_forget()
        self.u_dict["show_overdue"] = False
        self.od_toggle.configure(text="show",
                                 command=self.show_overdue)

    def show_overdue(self):
        """Pack overdue list, set user show_overdue to true, change button"""
        self.od_list.pack()
        self.u_dict["show_overdue"] = True
        self.od_toggle.configure(text="hide",
                                 command=self.hide_overdue)

    def display_tasks(self,
                      task_frame: tk.Frame,
                      list_to_disp: list[tc.Task],
                      u_tasks: list[tc.Task]) ->list[TaskDisp]:
        """Create a list of taskdisps with input parent frame from input list of tasks,
        put them all in a list"""
        out_list = []
        for task in list_to_disp:
            out_list.append(TaskDisp(task_frame,
                                     task.t_id,
                                     u_tasks,
                                     self.t_editor))
        return out_list

    def update(self):
        """Update and pack all frames in daily to-do, using input tasklist.
        - destroy all frames in overdue and today
        - rebuild all frames in overdue and today from new tasklist"""

        #Destroy taskdisp frames in overdue
        for od_disp in self.od_disps:
            od_disp.disp_frame.destroy()
        #Rebuild taskdisp frames in overdue
        self.od_tasks = tc.get_overdue(self.tasks, self.today)
        self.od_disps = self.display_tasks(self.od_list,
                                           self.od_tasks,
                                           self.tasks)
        for od_disp in self.od_disps:
            od_disp.disp_frame.pack()
        if self.u_dict["show_overdue"]:
            self.od_list.pack()
        #udpate count
        self.od_title.configure(text=f"{len(self.od_tasks)} unfinished tasks overdue.")

        #Destroy taskdisp frames in today
        for td_disp in self.td_disps:
            td_disp.disp_frame.destroy()

        #Rebuild taskdisp frames in today
        self.td_tasks = tc.get_today(self.tasks, self.today)
        self.td_disps = self.display_tasks(self.td_list,
                                           self.td_tasks,
                                           self.tasks)
        for td_disp in self.td_disps:
            td_disp.disp_frame.pack()
        self.td_list.pack()

        #update count
        self.td_title.configure(text=f"{len(self.td_tasks)} tasks due today.")


    def end_prgm(self):
        """Save changes to tasklist to json file, close all frames and windows."""

        #Update task list
        self.od_tasks = []
        for od_task_disp in self.od_disps:
            self.od_tasks.append(od_task_disp.task)
            print (od_task_disp.task.completed)

        self.td_tasks = []
        for td_task_disp in self.td_disps:
            self.td_tasks.append(td_task_disp.task)
            print(td_task_disp.task.t_id)

        changed_tasks = self.od_tasks + self.td_tasks
        for old_task in self.tasks:
            for new_task in changed_tasks:
                if new_task.t_id == old_task.t_id:
                    print(f"Found original task with id {old_task.t_id}")
                    old_task = new_task
                    print(f"Task completed: {old_task.completed}")

        # Pack current task list to json file
        task_list_dict: list[dict] = []
        for in_task in self.tasks:
            task_dict = {
                "id": in_task.t_id,
                "title": in_task.title,
                "dday": in_task.due.day,
                "dmonth": in_task.due.month,
                "dyear": in_task.due.year,
                "parent": in_task.t_parent,
                "subtasks": in_task.t_subs,
                "priority": in_task.priority,
                "completed": in_task.completed
            }
            task_list_dict.append(task_dict)
        self.task_data = {
            "users": [
                {
                    "uname": self.u_dict["uname"], #change later
                    "task_count": len(task_list_dict),
                    "show_overdue": self.u_dict["show_overdue"],
                    "tasks": task_list_dict
                }
            ]
        }

        json_tasks = json.dumps(self.task_data, indent=4)
        #write to json file
        with open("tasks.json", mode="w", encoding="utf-8") as outfile:
            outfile.write(json_tasks)

        #Destroy all tk objects
        self.window.destroy()
