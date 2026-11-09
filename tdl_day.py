"""Contains object class for the daily to-do list and subclass for task displays."""

import json
from datetime import date as dt
import tkinter as tk
import task_class as tc
from task_editor import TaskEdit, new_parent, new_subs

edit_task: tc.Task = None
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
                 u_tasks: list[tc.Task]):
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

    def mark_done(self, u_tasks:list[tc.Task]):
        """Set task complete to true, remove task from list"""
        self.task.completed = True
        #replace original task
        for task in u_tasks:
            if task.t_id == self.task.t_id:
                task = self.task
        #Remove task display from parent
        self.disp_frame.destroy()

class EtaskDisp:
    """EtaskDisp contains info regarding:
    - Parent Frame (input)
    - Display Task (input)
    - Dispframe
    - Select buttton"""

    def __init__(self,
                 root: tk.Frame,
                 disp_task: tc.Task):
        self.disp_frame = tk.Frame(root)
        self.disp_task = disp_task
        self.select_btn = tk.Button(self.disp_frame,
                                    text=disp_task.title,
                                    command=lambda: self.task_sel(root))
        self.select_btn.pack()

    def task_sel(self, root: tk.Frame):
        """Set edittask to disptask, close root frame"""
        global edit_task
        edit_task = self.disp_task
        root.pack_forget()


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
                 te_frame: tk.Frame,
                 ):
        """Using input arguments, create remaining data"""
        #Set input values
        self.window = window
        self.root = root
        self.u_dict = {}
        self.t_editor = None
        self.today = today
        self.task_data = {}
        self.tasks = []
        self.user_check = user_check
        self.te_frame = te_frame

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

        #Delete Button
        self.task_delete_btn = tk.Button(self.root,
                                            text="Exit Without Saving (Delete Task)",
                                            command=self.task_deleter)

        #Edit Tasks button
        self.edit_tasks: list[EtaskDisp] = []
        self.edit_btn = tk.Button(self.root,
                                  text="Edit a task",
                                  command=self.show_etasks)
        self.edit_btn.pack()

        #Edit List Frame
        self.edit_frame = tk.Frame(self.root)
        self.edit_title = tk.Label(self.edit_frame, text="Select a task to edit, then click enter.\n If no task selected, return to main screen.")
        self.edit_title.pack()

        #Close Button
        self.quit_btn = tk.Button(self.root,
                                  text="Close Dewitt",
                                  command= self.end_prgm)
        self.quit_btn.pack()

    def task_edit(self):
        """Set main window to editor display, input newtask info to editor"""
        self.edit_btn.configure(command=self.show_etasks)
        self.edit_frame.pack_forget()
        self.edit_btn.pack_forget()
        self.quit_btn.pack_forget()
        if edit_task is None:
            #Close edit list, reopen main frames

            self.header.pack()
            self.od_frame.pack()
            self.td_frame.pack()
            self.edit_btn.pack()
            self.quit_btn.pack()
        else:
            #Set main window to edit display
            self.save_btn.pack()
            self.task_delete_btn.pack()
            self.quit_btn.pack()

            #Create new teditor
            self.t_editor = TaskEdit(self.te_frame, 0, self.tasks)

            #Send edittask data to taskeditor
            self.t_editor.title_var.set(edit_task.title)
            self.t_editor.day_var.set(edit_task.due.day)
            self.t_editor.month_var.set(edit_task.due.month)
            self.t_editor.year_var.set(edit_task.due.year)
            self.t_editor.priority_var.set(edit_task.priority)
            self.t_editor.task_id = edit_task.t_id
            self.t_editor.t_parent = edit_task.t_parent
            self.t_editor.subs = edit_task.t_subs
            global new_parent, new_subs
            new_subs = []
            new_parent = None
            for sub_id in edit_task.t_subs:
                in_sub = tc.get_task_by_id(self.tasks, sub_id)
                if in_sub is None:
                    edit_task.t_subs.remove(in_sub)
                    
            self.t_editor.update_ps(self.tasks)

            #Pack editor frame
            self.t_editor.e_frame.grid(row=0, column=self.t_editor.grid_to_col)


    def show_etasks(self):
        """Close all other frames on main display. Open a list of editordisps with buttons that
        send you to editor with that task's info."""

        #Hide main frames
        self.header.pack_forget()
        self.od_frame.pack_forget()
        self.td_frame.pack_forget()
        self.edit_btn.pack_forget()

        #Destroy old task list
        for old_task in self.edit_tasks:
            old_task.disp_frame.destroy()

        #Show editable tasks
        global edit_task
        edit_task = None
        for disp_task in self.od_tasks + self.td_tasks:
            ed = EtaskDisp(self.edit_frame, disp_task)
            self.edit_tasks.append(ed)
            ed.disp_frame.pack()
        self.edit_frame.pack()
        self.edit_btn.pack()

        #Change edit button
        self.edit_btn.configure(command=self.task_edit)


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


        if not check_day.isdigit():
            return (False, "ERROR: day must be a number.")

        if not check_month.isdigit():
            return (False, "ERROR: month must be a number.")

        if not check_year.isdigit():
            return (False, "ERROR: year must be a number.")

        if not check_priority.isdigit():
            return (False, "ERROR: priority must be a number.")

        try:
            dt(int(check_year), int(check_month), int(check_day))
        except ValueError:
            return (False, "ERROR: Must input a valid date.")

        if int(check_priority) not in range(0, 11):
            return (False, "ERROR: Priority must be between 0 and 10.")

        return (True, "")

    def get_highest_id(self) -> int:
        """Set task count to highest id"""
        highest = 0
        for task in self.tasks:
            if task.t_id > highest:
                highest = task.t_id
        return highest


    def save(self, ptask_edit: TaskEdit):
        """- Validate input
        - Recursively save all subtasks in task, then save task"""
        self.u_dict["task_count"] = self.get_highest_id()
        if self.t_editor is not None:
            #Get entry values
            in_month = self.t_editor.month_var.get()
            in_day = self.t_editor.day_var.get()
            in_year = self.t_editor.year_var.get()
            in_priority = self.t_editor.priority_var.get()

            input_valid = self.input_validate(in_day, in_month, in_year, in_priority)
            if input_valid[0]:
                
                for sub_te in ptask_edit.sub_editors:
                    self.save(sub_te)
                ptask_edit.errors.pack_forget()

                #Create new task from input
                if ptask_edit.task_id is None:
                    self.u_dict["task_count"] += 1
                    ptask_edit.task_id = self.u_dict["task_count"]

                new_task = tc.Task(ptask_edit.task_id,
                                    ptask_edit.title_var.get(),
                                    dt(int(in_year), int(in_month), int(in_day)),
                                    ptask_edit.subs,
                                    int(in_priority),
                                    False,
                                    ptask_edit.t_parent
                                    )

                #Destroy editor frame if all sub editors are also hidden
                all_subs_valid = True
                for sub_te in ptask_edit.sub_editors:
                    if sub_te.e_frame.winfo_exists():
                        all_subs_valid = False
                    else:
                        new_task.t_subs.append(sub_te.task_id)
                        ptask_edit.sub_editors.remove(sub_te)
                if all_subs_valid:
                    ptask_edit.e_frame.destroy()

                #Add newtask if not already existing, replace if existing
                is_in_tasks = False
                for check_task in self.tasks:
                    if check_task.t_id == new_task.t_id:
                        self.tasks[self.tasks.index(check_task)] = new_task
                        is_in_tasks = True
                if not is_in_tasks:
                    self.tasks.append(new_task)
                for sub_id in new_task.t_subs:
                    tc.get_task_by_id(self.tasks, sub_id).t_parent = new_task.t_id
                self.u_dict["task_count"] = self.get_highest_id()
                
            else:
                ptask_edit.errors.configure(text=input_valid[1])
                ptask_edit.errors.pack()


    def save_task(self):
        """After validating input, either return an error message or:
        - create a new task from input fields and current set id
        - add new task to main window task list
        - update main window
        - hide editor window"""
        global edit_task
        edit_task = None
        if self.t_editor is not None:
            #Get entry values
            self.save(self.t_editor)

            #Destroy editor frame, return to main
            if self.t_editor.e_frame.winfo_exists():
                self.t_editor.e_frame.destroy()
            self.t_editor = None
        #Reset Main window

        self.save_btn.pack_forget()
        self.task_delete_btn.pack_forget()
        self.quit_btn.pack_forget()

        self.update()
        self.header.pack()
        self.od_frame.pack()
        self.td_frame.pack()
        self.edit_btn.pack()
        self.quit_btn.pack()
            

    def task_create(self):
        """Open Task Creator menu with date input reflecting current date,
        all other fields empty."""

        self.t_editor = TaskEdit(self.te_frame, 0, self.tasks)

        if self.t_editor is not None:
            #set fields
            global edit_task
            self.t_editor.title_var.set("")
            self.t_editor.month_var.set(self.today.month)
            self.t_editor.day_var.set(self.today.day)
            self.t_editor.year_var.set(self.today.year)
            self.t_editor.priority_var.set(0)
            self.t_editor.parent_label.configure(text="No Parent task selected.")

            self.t_editor.show_window()
            self.t_editor.e_frame.grid(row=0, column=self.t_editor.grid_to_col)

            self.header.pack_forget()
            self.od_frame.pack_forget()
            self.td_frame.pack_forget()
            self.edit_btn.pack_forget()
            self.quit_btn.pack_forget()

            self.save_btn.pack()
            self.task_delete_btn.pack()
            self.quit_btn.pack()

    def task_delete(self, dest_edit: TaskEdit):
        """Remove task with id taskid (in taskeditor) from tasks
        close editor frames, open main frames"""
        #Operate recursively over subtask editor frames
        for eframe in dest_edit.sub_editors:
            self.task_delete(eframe)

        #Remove task if it already exists
        rem_task = tc.get_task_by_id(self.tasks, dest_edit.task_id)
        if rem_task is not None:
            #Set parent and sub connections to none
            if rem_task.t_id in tc.get_task_by_id(self.tasks, rem_task.t_parent).t_subs:
                tc.get_task_by_id(self.tasks, rem_task.t_parent).t_subs.remove(rem_task.t_id)
            for sub_id in rem_task.t_subs:
                tc.get_task_by_id(self.tasks, sub_id).t_parent = None

            self.tasks.remove(rem_task)

        #Close e frames
        dest_edit.e_frame.destroy()

        

    def task_deleter(self):
        """Run recursive taskdelete, return to main display"""
        self.task_delete(self.t_editor)

        #open updated m frames
        self.update()
        self.save_btn.pack_forget()
        self.quit_btn.pack_forget()
        self.task_delete_btn.pack_forget()
        self.header.pack()
        self.od_frame.pack()
        self.td_frame.pack()
        self.edit_btn.pack()
        self.quit_btn.pack()

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
                                     u_tasks,))
        return out_list

    def sort_by_priority(self,
                         unsorted: list[tc.Task]) -> list[tc.Task]:
        """Run input unsorted list through an insertion sort based on their priority."""
        sorted_list: list[tc.Task] = []
        for in_task in unsorted:
            for check_task in sorted_list:
                if in_task.priority < check_task.priority:
                    sorted_list.insert(sorted_list.index(check_task), in_task)
                    break
            if in_task not in sorted_list:
                sorted_list.append(in_task)
        return sorted_list

    def update(self):
        """Update and pack all frames in daily to-do, using input tasklist.
        - destroy all frames in overdue and today
        - rebuild all frames in overdue and today from new tasklist"""

        #Destroy taskdisp frames in overdue
        for od_disp in self.od_disps:
            od_disp.disp_frame.destroy()
        #Rebuild taskdisp frames in overdue
        self.od_tasks = tc.get_overdue(self.tasks, self.today)
        self.od_tasks = self.sort_by_priority(self.od_tasks)
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
        self.td_tasks = self.sort_by_priority(self.td_tasks)
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

        self.td_tasks = []
        for td_task_disp in self.td_disps:
            self.td_tasks.append(td_task_disp.task)

        changed_tasks = self.od_tasks + self.td_tasks
        for old_task in self.tasks:
            for new_task in changed_tasks:
                if new_task.t_id == old_task.t_id:
                    old_task = new_task

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
        if len(task_list_dict) < self.u_dict["task_count"]:
            new_count = self.u_dict["task_count"]
        else:
            new_count = len(task_list_dict)
        self.task_data = {
            "users": [
                {
                    "uname": self.u_dict["uname"], #change later
                    "task_count": new_count,
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
