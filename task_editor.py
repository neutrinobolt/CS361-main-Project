"""Contains object class for task editor windows"""

from datetime import date as dt
import tkinter as tk
import task_class as tc

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
                 utasks: list[tc.Task]):

        self.grid_to_col = grid_to_col
        self.task_id:int = None
        self.out_task: tc.Task = None
        self.output_ready = False
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

        #Parent Input
        self.parent_frame = tk.Frame(self.e_frame)
        self.parent_label= tk.Label(self.parent_frame)
        self.t_parent = None
        self.parent_picker = tk.Button(self.e_frame,
                                       text="Choose a Parent Task",
                                       command=lambda: self.show_p_list())
        self.parent_label.pack()
        self.parent_picker.pack()
        self.parent_frame.pack()

        #Subtask Input
        self.sub_frame = tk.Frame(self.e_frame)
        self.sub_title = tk.Label(self.sub_frame)
        self.sub_list = tk.Frame(self.sub_frame)
        self.subs = []
        self.add_sub_btn = tk.Button(self.sub_frame,
                                     text="Add Subtask",
                                     command=lambda:self.show_s_list())
        self.sub_title.pack()
        self.sub_list.pack()
        self.add_sub_btn.pack()
        self.sub_frame.pack()

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

        #Delete Button
        self.task_delete_btn = tk.Button(self.e_frame,
                                         text="Exit Without Saving (Delete Task)",
                                         command=lambda:self.task_delete())
        self.task_delete_btn.pack()

    def show_p_list(self):
        print("function show_p_list not yet written.")

    def show_s_list(self):
        print("function show_s_list not yet written.")


    def task_delete(self):
        print("Function task_delete not yet written.")

    def show_parent(self, in_task: tc.Task):
        print("function show_parent not yet written.")

    def show_subs(self, in_task: tc.Task):
        print("function show_subs not yet written.")
