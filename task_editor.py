"""Contains object class for task editor windows"""

import tkinter as tk
import task_class as tc

new_parent:int = None
new_subs:list[tc.Task] = []
class EditDisp:
    """EditDisp holds data for a frame containing a task title, and a button
    that adds that task to an output task.
    - eDisp Data:
        - in task (given on init)
        - out tasklist (given on init)
        - root frame (given on init)
        - display frame
        - title label
        - add task button
    - eDisp functions:
        - add task to out list
    """
    def __init__(self,
                 disp_task: tc.Task,
                 root: tk.Frame,
                 output_case: str,
                 upper_tid: int,
                 u_tasks: list[tc.Task]
                 ):
        #Derived variables
        self.in_task = disp_task
        self.ed_frame = tk.Frame(root)

        # Tk objects
        self.ed_title = tk.Label(self.ed_frame, text=self.in_task.title)
        self.ed_title.grid(row=0, column=0)

        self.add_btn = tk.Button(self.ed_frame,
                                 text="select",)
        match output_case:
            case "set_parent":
                self.add_btn.configure(command=lambda:self.set_parent(disp_task, root, u_tasks))
            case "set_sub":
                self.add_btn.configure(command=lambda:self.set_sub(disp_task, root, upper_tid, u_tasks))
        self.add_btn.grid(row=0, column=1)

        self.ed_frame.pack()

    def set_sub(self, disp_task: tc.Task, root: tk.Frame, upper_tid: int, u_tasks: list[tc.Task]):
        """append disp task to upper task subs, set upper task id to parent of disp task,
        destroy frame"""
        new_subs.append(disp_task.t_id)
        u_tasks[u_tasks.index(disp_task)].t_parent = upper_tid
        
        root.destroy()

    def set_parent(self, disp_task: tc.Task, root: tk.Frame, u_tasks: list[tc.Task]):
        """set disp task to parent of upper task, append upper task id to disp subs,
        destroy frame"""
        global new_parent
        new_parent = disp_task.t_id
        u_tasks[u_tasks.index(tc.get_task_by_id(u_tasks, disp_task.t_id))].t_subs.append(disp_task.t_id)
        root.destroy()

class SubDisp:
    """SubDisp contains:
    - Frame connected to parent (input)
    - Title of input task
    - Remove button
    - Remove function
    """
    def __init__(self,
                 root: tk.Frame,
                 disp_task: tc.Task,
                 u_tasks: list[tc.Task]):
        self.disp_frame = tk.Frame(root)
        self.disp_frame.pack()
        self.sub_name = tk.Label(self.disp_frame, text=disp_task.title)
        self.sub_name.grid(row=0, column=0)
        self.remove_btn = tk.Button(self.disp_frame, text="Remove subtask",
                                    command=lambda:self.remove_sub(u_tasks, disp_task))
        self.remove_btn.grid(row=0, column=1)

    def remove_sub(self, u_tasks: list[tc.Task], disp_task: tc.Task):
        """Disconnect disp task from its parent, destroy disp frame"""
        if disp_task.t_parent is not None:
            u_tasks[u_tasks.index(tc.get_task_by_id(u_tasks, disp_task.t_parent))].t_subs.remove(disp_task.t_id)
        u_tasks[u_tasks.index(disp_task)].t_parent = None

        self.disp_frame.destroy()

class TaskEdit:
    """TaskEdit contains info regarding:
    - Parent Frame (input)
    - Daily todo (input)
    - Full Task List (input)
    - User Dict (input)
    - task id (input)
    - subtask editor frame (input)
    - Current Date (input)
    - Column grid (input)
    - Derived values:
        - Frame Header
        - Title Input Frame
        - Date Input Frame
        - Parent task Input Frame
        - Subtask Input Frame
        - Priority Input Frame
        - Save Task Button
        - Delete Task Button
    - functions:
        - input validation
        - display list of potential parents
        - display list of potential subtasks
        - add parent
        - remove parent
        - add subtask
        - remove subtask
        - save task
        - delete task
    """
    def __init__(self,
                 root: tk.Frame,
                 grid_to_col: int,
                 u_tasks: list[tc.Task]):

        self.grid_to_col = grid_to_col
        self.task_id:int = None
        self.out_task: tc.Task = None
        self.output_ready = False
        self.sub_editors: list[TaskEdit] = []
        #Setup frame
        self.e_frame = tk.Frame(root)
        #Header
        self.head = tk.Frame(self.e_frame)
        self.h_title = tk.Label(self.head)
        if grid_to_col > 0:
            self.h_title.configure(text="Subtask Details")
        else:
            self.h_title.configure(text="Task Details")
        self.h_title.pack()
        self.errors = tk.Label(self.head)
        self.head.pack()

        #Title Entry
        self.title_frame = tk.Frame(self.e_frame)
        self.title_label = tk.Label(self.title_frame, text="Task Name")
        self.title_label.grid(row=0, column=0)
        self.title_var = tk.StringVar()
        self.title_entry = tk.Entry(self.title_frame,
                           textvariable= self.title_var,
                           font=('calibre',10, 'normal'))
        self.title_entry.grid(row=0, column=1)
        self.title_frame.pack()

        #Date Entry
        self.date_frame = tk.Frame(self.e_frame)
        self.date_title = tk.Label(self.date_frame, text="Due Date")
        self.date_title.pack()
        self.dentry = tk.Frame(self.date_frame)
        self.month_var = tk.StringVar()
        self.day_var = tk.StringVar()
        self.year_var = tk.StringVar()
        self.month_entry = tk.Entry(self.dentry, textvariable=self.month_var)
        self.day_entry = tk.Entry(self.dentry, textvariable=self.day_var)
        self.year_entry = tk.Entry(self.dentry, textvariable=self.year_var)
        self.month_label = tk.Label(self.dentry, text="month", font=('calibre',10, 'bold'))
        self.day_label = tk.Label(self.dentry, text="day", font=('calibre',10, 'bold'))
        self.year_label = tk.Label(self.dentry, text="year", font=('calibre',10, 'bold'))

        self.month_entry.grid(row=0, column=0)
        self.day_entry.grid(row=0, column=1)
        self.year_entry.grid(row=0, column=2)
        self.month_label.grid(row=1, column=0)
        self.day_label.grid(row=1, column=1)
        self.year_label.grid(row=1, column=2)

        self.dentry.pack()
        self.date_frame.pack()

        self.task_list_f: tk.Frame = tk.Frame(root)
        self.task_list: list[EditDisp] = []

        #Return Button
        self.return_btn = tk.Button(self.e_frame, text="Return to Editor",
                                    command=lambda:self.update_ps(u_tasks))

        #Parent Input
        self.parent_frame = tk.Frame(self.e_frame)
        self.parent_label= tk.Label(self.parent_frame)
        self.t_parent: int = None
        self.parent_picker = tk.Button(self.parent_frame,
                                       text="Choose a Parent Task",
                                       command=lambda: self.show_p_list(u_tasks, root))
        self.parent_label.pack()
        self.parent_picker.pack()
        self.parent_frame.pack()

        #Subtask Input
        self.sub_frame = tk.Frame(self.e_frame)
        self.sub_title = tk.Label(self.sub_frame)
        self.sub_list = tk.Frame(self.sub_frame)
        self.subs: list[int] = []
        self.add_sub_btn = tk.Button(self.sub_frame,
                                     text="Add Subtask",
                                     command=lambda:self.show_s_list(u_tasks, root))
        self.sub_title.pack()
        self.sub_list.pack()
        self.add_sub_btn.pack()
        self.sub_frame.pack()

        #New Subtask Creator
        self.new_sub_btn = tk.Button(self.sub_frame, text="Create new subtask", command=lambda: self.sub_edit(root, u_tasks))
        self.new_sub_btn.pack()

        #Priority Entry
        self.priority_frame = tk.Frame(self.e_frame)
        self.priority_title = tk.Label(self.priority_frame,
                                       text="Priority Level (0-10, 0 is highest priority)")
        self.priority_var = tk.StringVar()
        self.priority_entry = tk.Entry(self.priority_frame,
                                       textvariable=self.priority_var,
                                       font=('calibre',10, 'bold'))

        self.priority_title.pack()
        self.priority_entry.pack()
        self.priority_frame.pack()

    def sub_edit(self, root: tk.Frame, u_tasks: list[tc.Task]):
        """Create a new Taskedit, grid next to this one. Set values to default, but don't show the
        change parent button."""
        #create sub taskedit
        new_te = TaskEdit(root, self.grid_to_col + 2, u_tasks)
        new_te.day_var.set(self.day_var.get())
        new_te.month_var.set(self.month_var.get())
        new_te.year_var.set(self.year_var.get())
        new_te.priority_var.set(self.priority_var.get())
        new_te.parent_label.configure(text=f"Parent: {self.title_var.get()}")
        new_te.parent_picker.pack_forget()
        new_te.t_parent = self.task_id

        #Grid new taskedit and append to self. sublist
        self.sub_editors.append(new_te)
        new_te.e_frame.grid(row=0, column=new_te.grid_to_col)

    def update_ps(self, u_tasks: list[tc.Task]):
        """Reopen frame with new parent and sub values for current task id"""

        #Close any edisp frames still open
        if self.task_list_f.winfo_exists():
            for ed_frame in self.task_list_f.winfo_children():
                ed_frame.destroy()
            self.task_list = []

        #Bring back main frames
        self.return_btn.pack_forget()
        self.head.pack()
        self.title_frame.pack()
        self.date_frame.pack()
        self.parent_frame.pack()
        self.sub_frame.pack()
        self.priority_frame.pack()

        #Write parent and subs
        self.subs += new_subs
        self.t_parent = new_parent

        if self.t_parent is not None:
            ptask = tc.get_task_by_id(u_tasks, self.t_parent)
            if ptask is not None:
                self.parent_label.configure(text=f"Parent: {ptask.title}")
            else:
                self.parent_label.configure(text="No Parent Selected.")
                self.t_parent = None
        else:
            self.parent_label.configure(text="No Parent Selected.")

        self.show_subs(u_tasks)

    def show_p_list(self, u_tasks: list[tc.Task], root: tk.Frame):
        """Create a list of all incomplete tasks in editdisps.
        Set so that selecting a taskedit sets current task parent to that task."""
        self.task_list_f = tk.Frame(root)
        for check_task in u_tasks:
            if not check_task.completed and check_task.t_id != self.task_id and check_task.t_id not in self.subs:
                new_edisp = EditDisp(check_task, self.task_list_f,
                                     "set_parent",
                                     self.task_id,
                                     u_tasks)
                new_edisp.ed_frame.pack()
                self.task_list.append(new_edisp)
        self.task_list_f.grid(row=0, column=self.grid_to_col + 1)
        self.return_btn.pack()

        self.head.pack_forget()
        self.title_frame.pack_forget()
        self.date_frame.pack_forget()
        self.parent_frame.pack_forget()
        self.sub_frame.pack_forget()
        self.priority_frame.pack_forget()

    def show_s_list(self, u_tasks: list[tc.Task], root: tk.Frame):
        """Pack editdisps of all incomplete tasks to tasklistf.
        set taskedit button to set_sub"""
        self.task_list_f = tk.Frame(root)
        for check_task in u_tasks:
            if not check_task.completed and check_task.t_id != self.task_id and check_task.t_id not in self.subs:
                new_edisp = EditDisp(check_task, self.task_list_f,
                                     "set_sub",
                                     self.task_id,
                                     u_tasks)
                new_edisp.ed_frame.pack()
        self.task_list_f.grid(row=0, column=self.grid_to_col + 1)
        self.return_btn.pack()

        self.head.pack_forget()
        self.title_frame.pack_forget()
        self.date_frame.pack_forget()
        self.parent_frame.pack_forget()
        self.sub_frame.pack_forget()
        self.priority_frame.pack_forget()

    def show_subs(self, u_tasks: list[tc.Task]):
        """Pack subdisp frames for every task in utasks that is a sub of selftaskid"""
        for frame in self.sub_list.winfo_children():
            frame.destroy()
        self.subs

        for sub_task_id in self.subs:
            sub_task = tc.get_task_by_id(u_tasks, sub_task_id)
            if sub_task is not None:
                new_disp_s = SubDisp(self.sub_list, sub_task, u_tasks)
                new_disp_s.disp_frame.pack()
            else:
                self.subs.remove(sub_task_id)

    def hide_window(self):
        """run pack_forget on all frames in object."""
        self.head.pack_forget()
        self.title_frame.pack_forget()
        self.date_frame.pack_forget()
        self.parent_frame.pack_forget()
        self.sub_frame.pack_forget()
        self.priority_frame.pack_forget()
        self.e_frame.pack_forget()

    def show_window(self):
        """Run pack on all frames in object."""
        self.head.pack()
        self.title_frame.pack()
        self.date_frame.pack()
        self.parent_frame.pack()
        self.sub_frame.pack()
        self.priority_frame.pack()
        self.e_frame.grid(row=0, column=self.grid_to_col)
