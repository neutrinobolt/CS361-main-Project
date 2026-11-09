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

import tkinter as tk
from datetime import date as dt
import tdl_day as td
# import task_editor as te

USER_CHECK = "test" #replace with login function when created

def main():
    """Main function. Set up window and frames, display day frame"""

    current_date = dt.today()

    window = tk.Tk()
    window.title("Dewitt")

    p_main = tk.Frame(window)
    t_editor = tk.Frame(window)

    day_obj = td.Daylist(window, p_main, USER_CHECK, current_date, t_editor)

    day_obj.update()

    p_main.grid(row=0, column=1)
    t_editor.grid(row=0, column=2)

    window.mainloop()

if __name__ == "__main__":
    main()
