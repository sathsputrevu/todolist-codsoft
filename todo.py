import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import json
from datetime import datetime
import tkinter

class TodoListApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Todo List App")
        self.configure(bg="#E6E6FA")

        # Calculate the center position of the screen
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x_coordinate = (screen_width - 700) / 2
        y_coordinate = (screen_height - 700) / 2

        self.geometry(f"700x700+{int(x_coordinate)}+{int(y_coordinate)}")

        self.task_input = ttk.Entry(self, font=("TkDefaultFont", 16), width=30)
        self.task_input.pack(pady=10)
        self.task_input.insert(0, "Enter your todo here...")
        self.task_input.configure(foreground="gray")
        self.task_input.bind("<FocusIn>", self.clear_placeholder)
        self.task_input.bind("<FocusOut>", self.restore_placeholder)
        self.task_input.bind("<Return>", lambda event: self.add_task())

        self.calendar = DateEntry(self, background="darkblue", foreground="white", borderwidth=2)
        self.calendar.pack(pady=5)

        self.add_button = ttk.Button(self, text="Add", command=self.add_task, style="Custom.TButton")
        self.add_button.pack(pady=5)

        self.task_list = tk.Listbox(self, font=("TkDefaultFont", 16), height=10, bg="#E6E6FA", selectbackground="#9370DB")
        self.task_list.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.task_list.bind("<Up>", self.move_up)
        self.task_list.bind("<Down>", self.move_down)

        self.mark_done_button = ttk.Button(self, text="Mark as Done", command=self.mark_done, style="Custom.TButton")
        self.mark_done_button.pack(side=tk.LEFT, padx=10, pady=5)
        self.remove_button = ttk.Button(self, text="Remove", command=self.remove_task, style="Custom.TButton")
        self.remove_button.pack(side=tk.LEFT, padx=10, pady=5)
        self.view_stats_button = ttk.Button(self, text="View Stats", command=self.view_stats, style="Custom.TButton")
        self.view_stats_button.pack(side=tk.RIGHT, padx=10, pady=5)

        self.style = ttk.Style()
        self.style.configure("Custom.TButton", background="#FFD700", foreground="#4B0082", font=("TkDefaultFont", 12), borderwidth=0)

        self.load_tasks()

    def view_stats(self):
        total_tasks = self.task_list.size()
        completed_tasks = sum(1 for i in range(total_tasks) if self.task_list.itemcget(i, "fg") == "green")
        overdue_tasks = sum(1 for i in range(total_tasks) if self.task_list.itemcget(i, "fg") == "red")
        messagebox.showinfo("Task Statistics", f"Total tasks: {total_tasks}\nCompleted tasks: {completed_tasks}\nOverdue tasks: {overdue_tasks}")

    def add_task(self):
        task = self.task_input.get()
        if task != "Enter your todo here...":
            deadline = self.calendar.get_date() 
            task_with_deadline = f"{task} ({deadline.strftime('%m/%d/%Y')})"
            if deadline < datetime.now().date(): 
                self.task_list.insert(tk.END, task_with_deadline)
                self.update_task_color(tk.END, "red") 
            else:
                self.task_list.insert(tk.END, task_with_deadline)
                self.update_task_color(tk.END, "orange") 
            self.task_input.delete(0, tk.END)
            self.save_tasks()

    def mark_done(self):
        task_index = self.task_list.curselection()
        if task_index:
            current_fg = self.task_list.itemcget(task_index[0], "fg")
            if current_fg != "green":
                self.task_list.itemconfig(task_index[0], fg="green")
            self.save_tasks()

    def remove_task(self):
        task_index = self.task_list.curselection()
        if task_index:
            self.task_list.delete(task_index)
            self.save_tasks()

    def clear_placeholder(self, event):
        if self.task_input.get() == "Enter your todo here...":
            self.task_input.delete(0, tk.END)

    def restore_placeholder(self, event):
        if self.task_input.get() == "":
            self.task_input.insert(0, "Enter your todo here...")

    def load_tasks(self):
        try:
            with open("tasks.json", "r") as f:
                data = json.load(f)
                for task in data:
                    self.task_list.insert(tk.END, task["text"])
                    self.update_task_color(tk.END, task["color"])
        except FileNotFoundError:
            pass

    def save_tasks(self):
        data = []
        for i in range(self.task_list.size()):
            text = self.task_list.get(i)
            color = self.task_list.itemcget(i, "fg")
            data.append({"text": text, "color": color})
        with open("tasks.json", "w") as f:
            json.dump(data, f)

    def move_up(self, event):
        selected_index = self.task_list.curselection()
        if selected_index and selected_index[0] > 0:
            current_index = selected_index[0]
            self.task_list.selection_clear(0, tk.END)
            self.task_list.selection_set(current_index - 1)
            self.task_list.activate(current_index - 1)
            self.task_list.see(current_index - 1)

    def move_down(self, event):
        selected_index = self.task_list.curselection()
        if selected_index and selected_index[0] < self.task_list.size() - 1:
            current_index = selected_index[0]
            self.task_list.selection_clear(0, tk.END)
            self.task_list.selection_set(current_index + 1)
            self.task_list.activate(current_index + 1)
            self.task_list.see(current_index + 1)
    
    def update_task_color(self, index, color):
        self.task_list.itemconfig(index, fg=color)

if __name__ == '__main__':
    app = TodoListApp()
    app.mainloop()
