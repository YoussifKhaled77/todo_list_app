import tkinter as tk
import tkinter.ttk as ttk
import datetime
import json
import os

class ToDoList:
    def __init__(self, filename="todo.json"):
        self.filename = filename
        self.tasks = self.load_tasks()

    def load_tasks(self):

        if os.path.exists(self.filename):
            with open(self.filename, "r") as file:
                data = json.load(file)

            return {int(task_id): Task.from_dict(task_data) for task_id, task_data in data.items()}
        
        else:
            return {}

    def save_tasks(self):
        data = {task_id: task.to_dict() for task_id, task in self.tasks.items()}
        
        with open(self.filename, "w") as file:
            json.dump(data, file)

    def add_task(self, task_name, due_date=None):
        
        if not self.tasks:
            task_id = 1
        
        else:
            task_id = max(self.tasks.keys()) + 1
        task = Task(task_name, due_date)
        self.tasks[task_id] = task
        self.save_tasks()
        
        return task_id

    def view_tasks(self):
        return "\n".join([f"Task ID: {task_id}\n{task}\n" for task_id, task in self.tasks.items()])

    def update_task(self, task_id, task_name=None, due_date=None, status=None):
        
        if task_id in self.tasks:
            task = self.tasks[task_id]

            if task_name:
                task.task_name = task_name
            
            if due_date:
                task.due_date = due_date
            
            if status:
                task.status = status
            
            self.save_tasks()
            
            return f"Task {task_id} updated"
        
        else:
        
            return "Task not found"

    def delete_task(self, task_id):
        if task_id in self.tasks:
       
            del self.tasks[task_id]
            self.save_tasks()
       
            return f"Task {task_id} deleted"
       
        else:
       
            return "Task not found"

    def mark_as_done(self, task_id):
        if task_id in self.tasks:
            
            self.tasks[task_id].status = "Done"
            self.save_tasks()
            
            return f"Task {task_id} marked as done"
        
        else:
        
            return "Task not found"

    def overdue_tasks(self):
        today = datetime.date.today()
        overdue_tasks = [task for task in self.tasks.values() if task.due_date and task.due_date < today]
        
        return "\n".join([str(task) for task in overdue_tasks])

class Task:
    def __init__(self, task_name, due_date=None ):
        self.task_name = task_name
        self.due_date = due_date
        self.status = "Not Started"

    def __repr__(self):
        return f"Task Name: {self.task_name}\nDue Date: {self.due_date}\nStatus: {self.status}"

    def to_dict(self):
        return {
            "task_name": self.task_name,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "status": self.status
        }

    @classmethod
    def from_dict(cls, data):
        due_date = datetime.datetime.fromisoformat(data["due_date"]).date() if data["due_date"] else None
        return cls(data["task_name"], due_date)

class Program:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("To-Do List")
        self.root.configure(bg="#2b2b2b")

        self.todo = ToDoList()

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(pady=10, expand=True)

#back ground colors (grey)
        self.add_task_frame = tk.Frame(self.notebook, bg="#2b2b2b")
        self.view_tasks_frame = tk.Frame(self.notebook, bg="#2b2b2b")
        self.update_task_frame = tk.Frame(self.notebook, bg="#2b2b2b")
        self.delete_task_frame = tk.Frame(self.notebook, bg="#2b2b2b")
        self.mark_as_done_frame = tk.Frame(self.notebook, bg="#2b2b2b")
        self.overdue_tasks_frame = tk.Frame(self.notebook, bg="#2b2b2b")


        self.notebook.add(self.add_task_frame, text="Add Task")
        self.notebook.add(self.view_tasks_frame, text="View Tasks")
        self.notebook.add(self.update_task_frame, text="Update Task")
        self.notebook.add(self.delete_task_frame, text="Delete Task")
        self.notebook.add(self.mark_as_done_frame, text="Mark as Done")
        self.notebook.add(self.overdue_tasks_frame, text="Overdue Tasks")


        self.add_task_widgets()
        self.view_tasks_widgets()
        self.update_task_widgets()
        self.delete_task_widgets()
        self.mark_as_done_widgets()
        self.overdue_tasks_widgets()


    def add_task_widgets(self):
        tk.Label(self.add_task_frame, text="Task Name:", bg="#2b2b2b", fg="#66ccff").pack()  
        self.add_task_name_entry = tk.Entry(self.add_task_frame, bg="#3b3b3b", fg="#ffffff", relief="ridge", bd=2) 
        self.add_task_name_entry.pack()

        tk.Label(self.add_task_frame, text="Due Date (YYYY-MM-DD):", bg="#2b2b2b", fg="#66ccff").pack()  
        self.add_task_due_date_entry = tk.Entry(self.add_task_frame, bg="#3b3b3b", fg="#ffffff", relief="ridge", bd=2)  
        self.add_task_due_date_entry.pack()

        self.add_task_button = tk.Button(self.add_task_frame, text="Add Task", command=self.add_task, bg="#4CAF50", width = 10 , fg="#ffffff", relief="ridge", bd=2)  
        self.add_task_button.pack()

        self.add_task_result_label = tk.Label(self.add_task_frame, text="", bg="#2b2b2b", fg="#66ccff")   
        self.add_task_result_label.pack()


    def view_tasks_widgets(self):
        self.view_tasks_text = tk.Text(self.view_tasks_frame, bg="#3b3b3b", fg="#ffffff", relief="ridge", bd=2)   
        self.view_tasks_text.pack()

        self.view_tasks_button = tk.Button(self.view_tasks_frame, text="View Tasks", command=self.view_tasks, bg="#0099ff", fg="#ffffff", relief="ridge", bd=2)   
        self.view_tasks_button.pack()


    def update_task_widgets(self):
        tk.Label(self.update_task_frame, text="Task ID:", bg="#2b2b2b", fg="#66ccff").pack()   
        self.update_task_id_entry = tk.Entry(self.update_task_frame, bg="#3b3b3b", fg="#ffffff", relief="ridge", bd=2)  
        self.update_task_id_entry.pack()

        tk.Label(self.update_task_frame, text="Task Name:", bg="#2b2b2b", fg="#66ccff").pack()   
        self.update_task_name_entry = tk.Entry(self.update_task_frame, bg="#3b3b3b", fg="#ffffff", relief="ridge", bd=2) 
        self.update_task_name_entry.pack()

        tk.Label(self.update_task_frame, text="Due Date (YYYY-MM-DD):", bg="#2b2b2b", fg="#66ccff").pack()   
        self.update_task_due_date_entry = tk.Entry(self.update_task_frame, bg="#3b3b3b", fg="#ffffff", relief="ridge", bd=2)   
        self.update_task_due_date_entry.pack()

        self.update_task_button = tk.Button(self.update_task_frame, text="Update Task", command=self.update_task, bg="#0099ff", fg="#ffffff", relief="ridge", bd=2)   
        self.update_task_button.pack()

        self.update_task_result_label = tk.Label(self.update_task_frame, text="", bg="#2b2b2b", fg="#66ccff")   
        self.update_task_result_label.pack()


    def delete_task_widgets(self):
        tk.Label(self.delete_task_frame, text="Task ID:", bg="#2b2b2b", fg="#66ccff").pack()   
        self.delete_task_id_entry = tk.Entry(self.delete_task_frame, bg="#3b3b3b", fg="#ffffff", relief="ridge", bd=2)  
        self.delete_task_id_entry.pack()

        self.delete_task_button = tk.Button(self.delete_task_frame, text="Delete Task", command=self.delete_task, bg="#ff3333", fg="#ffffff", relief="ridge", bd=2)   
        self.delete_task_button.pack()

        self.delete_task_result_label = tk.Label(self.delete_task_frame, text="", bg="#2b2b2b", fg="#66ccff")  
        self.delete_task_result_label.pack()


    def mark_as_done_widgets(self):
        tk.Label(self.mark_as_done_frame, text="Task ID:", bg="#2b2b2b", fg="#66ccff").pack() 
        self.mark_as_done_id_entry = tk.Entry(self.mark_as_done_frame, bg="#3b3b3b", fg="#ffffff", relief="ridge", bd=2)   
        self.mark_as_done_id_entry.pack()

        self.mark_as_done_button = tk.Button(self.mark_as_done_frame, text="Mark as Done", command=self.mark_as_done, bg="#33cc33", fg="#ffffff", relief="ridge", bd=2)   
        self.mark_as_done_button.pack()

        self.mark_as_done_result_label = tk.Label(self.mark_as_done_frame, text="", bg="#2b2b2b", fg="#66ccff")   
        self.mark_as_done_result_label.pack()

    def overdue_tasks_widgets(self):
        self.overdue_tasks_text = tk.Text(self.overdue_tasks_frame, bg="#3b3b3b", fg="#ffffff", relief="ridge", bd=2)  
        self.overdue_tasks_text.pack()

        self.overdue_tasks_button = tk.Button(self.overdue_tasks_frame, text="View Overdue Tasks", command=self.overdue_tasks, bg="#ff9900", fg="#ffffff", relief="ridge", bd=2)   
        self.overdue_tasks_button.pack()

    def add_task(self):
        task_name = self.add_task_name_entry.get()
        due_date_str = self.add_task_due_date_entry.get()
        try:
            if due_date_str:
                due_date = datetime.datetime.strptime(due_date_str, "%Y-%m-%d").date()
            else:
                due_date = None
            task_id = self.todo.add_task(task_name, due_date)
            self.add_task_result_label.config(text=f"\nTask '{task_name}' added with ID {task_id}")
        except ValueError:
            self.add_task_result_label.config(text="\nInvalid due date. Please enter a date in the format YYYY-MM-DD.")


    def view_tasks(self):
        tasks = self.todo.view_tasks()
        self.view_tasks_text.delete(1.0, tk.END)
        self.view_tasks_text.insert(tk.END, tasks)


    def update_task(self):
        task_id = self.update_task_id_entry.get()
        task_name = self.update_task_name_entry.get()
        due_date_str = self.update_task_due_date_entry.get()
        try:
            if due_date_str:
                due_date = datetime.datetime.strptime(due_date_str, "%Y-%m-%d").date()
            else:
                due_date = None
            result = self.todo.update_task(int(task_id), task_name, due_date)
            self.update_task_result_label.config(text=result)
        except ValueError:
            self.update_task_result_label.config(text="\nInvalid task ID or due date. Please enter a number for the task ID and a date in the format YYYY-MM-DD for the due date.")


    def delete_task(self):
        task_id = self.delete_task_id_entry.get()
        try:
            result = self.todo.delete_task(int(task_id))
            self.delete_task_result_label.config(text=result)
        except ValueError:
            self.delete_task_result_label.config(text="\nInvalid task ID. Please enter a number.")


    def mark_as_done(self):
        task_id = self.mark_as_done_id_entry.get()
        try:
            result = self.todo.mark_as_done(int(task_id))
            self.mark_as_done_result_label.config(text=result)
        except ValueError:
            self.mark_as_done_result_label.config(text="\nInvalid task ID. Please enter a number.")


    def overdue_tasks(self):
        tasks = self.todo.overdue_tasks()
        self.overdue_tasks_text.delete(1.0, tk.END)
        self.overdue_tasks_text.insert(tk.END, tasks)


    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    Program().run()
            
