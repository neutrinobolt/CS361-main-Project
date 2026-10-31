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
import tkinter as tk
from datetime import date as dt
from task_class import Task
import tdl_funcs as tdlf

USER_CHECK = "test" #replace with login function when created

def main():
    """Main function. Set up window and frames, display day frame"""

    current_date = dt.today()

    task_data = {}
    tasks:list[Task] = []
    user = {}

    od_tasks:list[Task] = []
    td_tasks:list[Task] = []

    #get json string
    with open("./tasks.json", mode="r", encoding="utf-8") as tfile:
        tdata_json = tfile.read()
        task_data = json.loads(tdata_json)

    #Get user task data
    for user in task_data["users"]:
        if user["uname"] == USER_CHECK:
            tasks_dict = user["tasks"]
            tasks = tdlf.taskify(tasks_dict)


    window = tk.Tk()
    window.title("Dewitt")

    ################################################################
    #Daily Tasks page display, initial setup
    ################################################################
    p_main = tk.Frame(window)
    overdue = tk.Frame(p_main)
    today = tk.Frame(p_main)

    t_editor = tk.Frame(window)

    #Header
    header = tk.Frame(p_main)
    title = tk.Label(header, text="To-Do Today")
    task_creator = tk.Button(header,
                            text="Create New Task",
                            command= lambda: tdlf.task_create(t_editor,
                                                              tasks,
                                                              user,
                                                              current_date,
                                                              overdue,
                                                              today,
                                                              od_tasks,
                                                              td_tasks,
                                                              error_msg=""))
    title.pack()
    task_creator.pack()

    header.pack()



    tdlf.update_day_tasks(overdue,
                          today,
                          tasks,
                          od_tasks,
                          td_tasks,
                          current_date,
                          user,
                          t_editor)

    overdue.pack()
    today.pack()

    quit_btn = tk.Button(p_main,text="Close Dewitt",
                        command=lambda: tdlf.end_prgm(tasks, od_tasks, td_tasks, user, window))
    quit_btn.pack()

    p_main.grid(row=0, column=1)
    t_editor.grid(row=0, column=2)

    window.mainloop()

if __name__ == "__main__":
    main()
