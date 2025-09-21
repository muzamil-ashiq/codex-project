import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import random
from PIL import Image, ImageTk, ImageDraw

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Autumn To-Do App")
        self.root.geometry("800x600")
        self.root.resizable(False, False)

        self.tasks = []
        self.task_file = "tasks.json"
        self.load_tasks()

        self.autumn_colors = {
            "bg_dark": "#4A2C2A",  # Dark Brown
            "bg_light": "#8B4513", # Saddle Brown
            "accent_orange": "#FF8C00", # Dark Orange
            "accent_yellow": "#DAA520", # Goldenrod
            "text_color": "#F5DEB3", # Wheat
            "button_bg": "#CD5C5C", # Indian Red
            "button_active_bg": "#B22222", # Firebrick
            "task_bg_even": "#A0522D", # Sienn
            "task_bg_odd": "#D2691E", # Chocolate
            "complete_text": "#7CFC00" # Lawn Green
        }

        self.setup_falling_leaves()
        self.setup_ui()

    def setup_ui(self):
        # Main frame for the entire application
        main_frame = tk.Frame(self.root, bg=self.autumn_colors["bg_dark"])
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Left menu frame
        self.menu_frame = tk.Frame(main_frame, bg=self.autumn_colors["bg_light"], width=200)
        self.menu_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        self.menu_frame.pack_propagate(False) # Prevent frame from resizing to content

        # Main content frame
        self.content_frame = tk.Frame(main_frame, bg=self.autumn_colors["bg_dark"])
        self.content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.create_menu_widgets()
        self.create_task_widgets()

    def create_menu_widgets(self):
        # Title for the menu
        menu_title = tk.Label(self.menu_frame, text="Options", font=("Arial", 16, "bold"),
                              bg=self.autumn_colors["bg_light"], fg=self.autumn_colors["text_color"])
        menu_title.pack(pady=10)

        # Add Task button
        add_task_btn = tk.Button(self.menu_frame, text="Add New Task", command=self.show_add_task_dialog,
                                 bg=self.autumn_colors["button_bg"], fg=self.autumn_colors["text_color"],
                                 font=("Arial", 12), relief=tk.FLAT, activebackground=self.autumn_colors["button_active_bg"])
        add_task_btn.pack(fill=tk.X, pady=5, padx=10)

        # Filter buttons (placeholder for now)
        all_tasks_btn = tk.Button(self.menu_frame, text="All Tasks", command=lambda: self.display_tasks("all"),
                                  bg=self.autumn_colors["button_bg"], fg=self.autumn_colors["text_color"],
                                  font=("Arial", 12), relief=tk.FLAT, activebackground=self.autumn_colors["button_active_bg"])
        all_tasks_btn.pack(fill=tk.X, pady=5, padx=10)

        pending_tasks_btn = tk.Button(self.menu_frame, text="Pending Tasks", command=lambda: self.display_tasks("pending"),
                                      bg=self.autumn_colors["button_bg"], fg=self.autumn_colors["text_color"],
                                      font=("Arial", 12), relief=tk.FLAT, activebackground=self.autumn_colors["button_active_bg"])
        pending_tasks_btn.pack(fill=tk.X, pady=5, padx=10)

        completed_tasks_btn = tk.Button(self.menu_frame, text="Completed Tasks", command=lambda: self.display_tasks("completed"),
                                        bg=self.autumn_colors["button_bg"], fg=self.autumn_colors["text_color"],
                                        font=("Arial", 12), relief=tk.FLAT, activebackground=self.autumn_colors["button_active_bg"])
        completed_tasks_btn.pack(fill=tk.X, pady=5, padx=10)

    def create_task_widgets(self):
        # Clear existing widgets in content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        task_list_title = tk.Label(self.content_frame, text="Your Tasks", font=("Arial", 18, "bold"),
                                   bg=self.autumn_colors["bg_dark"], fg=self.autumn_colors["text_color"])
        task_list_title.pack(pady=10)

        self.task_canvas = tk.Canvas(self.content_frame, bg=self.autumn_colors["bg_dark"], highlightthickness=0)
        self.task_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.task_scrollbar = ttk.Scrollbar(self.content_frame, orient="vertical", command=self.task_canvas.yview)
        self.task_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.task_canvas.configure(yscrollcommand=self.task_scrollbar.set)
        self.task_canvas.bind('<Configure>', lambda e: self.task_canvas.configure(scrollregion = self.task_canvas.bbox("all")))

        self.task_frame_inner = tk.Frame(self.task_canvas, bg=self.autumn_colors["bg_dark"])
        self.task_canvas.create_window((0, 0), window=self.task_frame_inner, anchor="nw", width=self.task_canvas.winfo_width())

        self.task_frame_inner.bind("<Configure>", lambda e: self.task_canvas.configure(scrollregion=self.task_canvas.bbox("all")))
        self.task_canvas.bind('<Configure>', self.on_canvas_resize)

        self.display_tasks("all")

    def on_canvas_resize(self, event):
        self.task_canvas.itemconfig(self.task_canvas.find_withtag("inner_frame_window"), width=event.width)

    def show_add_task_dialog(self):
        add_dialog = tk.Toplevel(self.root)
        add_dialog.title("Add New Task")
        add_dialog.geometry("300x150")
        add_dialog.transient(self.root) # Make dialog appear on top of main window
        add_dialog.grab_set() # Disable interaction with main window

        add_dialog.configure(bg=self.autumn_colors["bg_dark"])

        tk.Label(add_dialog, text="Task Description:", bg=self.autumn_colors["bg_dark"], fg=self.autumn_colors["text_color"]).pack(pady=10)
        task_entry = tk.Entry(add_dialog, width=40, bg=self.autumn_colors["text_color"], fg=self.autumn_colors["bg_dark"])
        task_entry.pack(pady=5)

        def add_and_close():
            description = task_entry.get().strip()
            if description:
                self.add_task(description)
                add_dialog.destroy()
            else:
                messagebox.showwarning("Input Error", "Task description cannot be empty.", parent=add_dialog)

        add_button = tk.Button(add_dialog, text="Add Task", command=add_and_close,
                               bg=self.autumn_colors["button_bg"], fg=self.autumn_colors["text_color"],
                               relief=tk.FLAT, activebackground=self.autumn_colors["button_active_bg"])
        add_button.pack(pady=10)

        add_dialog.bind("<Return>", lambda event: add_and_close()) # Bind Enter key
        task_entry.focus_set()

    def add_task(self, description):
        self.tasks.append({"description": description, "completed": False})
        self.save_tasks()
        self.display_tasks("all") # Refresh display

    def toggle_complete(self, index):
        self.tasks[index]["completed"] = not self.tasks[index]["completed"]
        self.save_tasks()
        self.display_tasks("all") # Refresh display

    def delete_task(self, index):
        if messagebox.askyesno("Delete Task", "Are you sure you want to delete this task?"):
            del self.tasks[index]
            self.save_tasks()
            self.display_tasks("all") # Refresh display

    def display_tasks(self, filter_type="all"):
        # Clear existing tasks from the inner frame
        for widget in self.task_frame_inner.winfo_children():
            widget.destroy()

        filtered_tasks = []
        if filter_type == "all":
            filtered_tasks = self.tasks
        elif filter_type == "pending":
            filtered_tasks = [task for task in self.tasks if not task["completed"]]
        elif filter_type == "completed":
            filtered_tasks = [task for task in self.tasks if task["completed"]]

        if not filtered_tasks:
            no_tasks_label = tk.Label(self.task_frame_inner, text="No tasks to display.",
                                      bg=self.autumn_colors["bg_dark"], fg=self.autumn_colors["text_color"],
                                      font=("Arial", 14))
            no_tasks_label.pack(pady=20)
            return

        for i, task in enumerate(filtered_tasks):
            task_bg = self.autumn_colors["task_bg_even"] if i % 2 == 0 else self.autumn_colors["task_bg_odd"]
            text_color = self.autumn_colors["complete_text"] if task["completed"] else self.autumn_colors["text_color"]

            task_row = tk.Frame(self.task_frame_inner, bg=task_bg, padx=10, pady=5)
            task_row.pack(fill=tk.X, pady=2)

            task_desc = tk.Label(task_row, text=task["description"], font=("Arial", 12),
                                 bg=task_bg, fg=text_color, anchor="w")
            task_desc.pack(side=tk.LEFT, fill=tk.X, expand=True)

            # Find the original index of the task in the self.tasks list
            original_index = self.tasks.index(task)

            complete_btn = tk.Button(task_row, text="✓" if task["completed"] else "○",
                                     command=lambda idx=original_index: self.toggle_complete(idx),
                                     bg=self.autumn_colors["button_bg"], fg=self.autumn_colors["text_color"],
                                     relief=tk.FLAT, activebackground=self.autumn_colors["button_active_bg"],
                                     width=3)
            complete_btn.pack(side=tk.RIGHT, padx=5)

            delete_btn = tk.Button(task_row, text="✗",
                                   command=lambda idx=original_index: self.delete_task(idx),
                                   bg=self.autumn_colors["button_bg"], fg=self.autumn_colors["text_color"],
                                   relief=tk.FLAT, activebackground=self.autumn_colors["button_active_bg"],
                                   width=3)
            delete_btn.pack(side=tk.RIGHT)

        # Update canvas scroll region after adding tasks
        self.task_frame_inner.update_idletasks()
        self.task_canvas.config(scrollregion=self.task_canvas.bbox("all"))
        self.task_canvas.create_window((0, 0), window=self.task_frame_inner, anchor="nw", tags="inner_frame_window")


    def load_tasks(self):
        if os.path.exists(self.task_file):
            with open(self.task_file, "r") as f:
                self.tasks = json.load(f)

    def save_tasks(self):
        with open(self.task_file, "w") as f:
                json.dump(self.tasks, f, indent=4)

    def setup_falling_leaves(self):
        self.leaf_images = []
        self.leaves = []
        self.num_leaves = 15 # Number of leaves to animate

        # Create a canvas for falling leaves effect, placed behind other widgets
        self.leaves_canvas = tk.Canvas(self.root, bg=self.autumn_colors["bg_dark"], highlightthickness=0)
        self.leaves_canvas.place(x=0, y=0, relwidth=1, relheight=1)


        # Ensure the resources directory exists
        resources_dir = "resources"
        if not os.path.exists(resources_dir):
            os.makedirs(resources_dir)

        # Create dummy leaf images if they don't exist
        leaf_paths = []
        for i in range(1, 4): # Create 3 types of leaves
            leaf_filename = os.path.join(resources_dir, f"leaf{i}.png")
            leaf_paths.append(leaf_filename)
            if not os.path.exists(leaf_filename):
                self.create_dummy_leaf_image(leaf_filename, i)

        for path in leaf_paths:
            try:
                img = Image.open(path)
                img = img.resize((30, 30), Image.LANCZOS) # Resize leaves
                self.leaf_images.append(ImageTk.PhotoImage(img))
            except FileNotFoundError:
                print(f"Warning: Leaf image not found at {path}. Falling leaves effect might be incomplete.")
                # Fallback: create a simple circle if image not found
                self.leaf_images.append(None) # Placeholder

        for _ in range(self.num_leaves):
            self.create_leaf()

        self.animate_leaves()

    def create_dummy_leaf_image(self, filename, type_id):
        # Create a simple colored circle as a dummy leaf
        img = Image.new('RGBA', (50, 50), (255, 0, 0, 0)) # Transparent background
        draw = ImageDraw.Draw(img)
        colors = ["#FF8C00", "#DAA520", "#CD5C5C"] # Orange, Yellow, Red
        color = colors[type_id - 1] if type_id <= len(colors) else colors[0]
        draw.ellipse((5, 5, 45, 45), fill=color)
        img.save(filename)
        print(f"Created dummy leaf image: {filename}")



    def create_leaf(self):
        x = random.randint(0, self.root.winfo_width() if self.root.winfo_width() > 0 else 800)
        y = random.randint(-50, 0) # Start above the screen
        speed = random.uniform(0.5, 2.0)
        rotation_speed = random.uniform(-5, 5) # For visual rotation effect (not actual image rotation)
        leaf_img = random.choice(self.leaf_images) if self.leaf_images else None
        if leaf_img:
            leaf_id = self.leaves_canvas.create_image(x, y, image=leaf_img, anchor="nw")
            self.leaves.append({"id": leaf_id, "x": x, "y": y, "speed": speed, "rotation_speed": rotation_speed, "image": leaf_img})
        else:
            # Fallback for when no images are loaded
            size = random.randint(10, 20)
            color = random.choice(list(self.autumn_colors.values())[2:5]) # Orange, Yellow, Red
            leaf_id = self.leaves_canvas.create_oval(x, y, x + size, y + size, fill=color, outline=color)
            self.leaves.append({"id": leaf_id, "x": x, "y": y, "speed": speed, "rotation_speed": rotation_speed, "image": None})


    def animate_leaves(self):
        canvas_height = self.root.winfo_height() if self.root.winfo_height() > 0 else 600
        canvas_width = self.root.winfo_width() if self.root.winfo_width() > 0 else 800

        for leaf in self.leaves:
            self.leaves_canvas.move(leaf["id"], 0, leaf["speed"])
            leaf["y"] += leaf["speed"]

            # Simple horizontal drift for more natural fall
            drift = random.uniform(-0.5, 0.5)
            self.leaves_canvas.move(leaf["id"], drift, 0)
            leaf["x"] += drift

            if leaf["y"] > canvas_height:
                # Reset leaf to top
                leaf["x"] = random.randint(0, canvas_width)
                leaf["y"] = random.randint(-50, 0)
                self.leaves_canvas.coords(leaf["id"], leaf["x"], leaf["y"])

        self.root.after(50, self.animate_leaves) # Animate every 50ms

if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()
