import tkinter as tk
from tkinter import messagebox
import winsound
import matplotlib.pyplot as plt
from PIL import Image, ImageTk
from tkinter import Tk, Label, SOLID, Entry, Button


class PageReplacementApp:
    def __init__(self, root):
         # List to store label widgets
        self.root = root
        self.row = 8 
        self.root.title("Page Replacement")
        self.root.geometry("1000x800")

        # Variables to store user input
        self.frames_var = tk.StringVar()
        self.reference_var = tk.StringVar()
        self.algorithm_var = tk.StringVar()

        # Font settings
        self.default_font = ("Arial", 14)

        # Colors for frame backgrounds
        self.frame_colors = ["#ff9999", "#99ff99", "#9999ff", "#ffff99", "#99ffff", "#ff99ff"]

        # GUI Elements
        frame = tk.Frame(root)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(frame, text="Number of Frames:", font=self.default_font).grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.frames_entry = tk.Entry(frame, textvariable=self.frames_var, font=self.default_font)
        self.frames_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame, text="Reference String (comma-separated):", font=self.default_font).grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.reference_entry = tk.Entry(frame, textvariable=self.reference_var, font=self.default_font)
        self.reference_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame, text="Page Replacement Algorithm:", font=self.default_font).grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.algorithm_menu = tk.OptionMenu(frame, self.algorithm_var, "FIFO", "LRU", "Optimal", "MRU")
        self.algorithm_menu.config(font=self.default_font)
        self.algorithm_menu.grid(row=2, column=1, padx=5, pady=5)

        self.run_button = tk.Button(frame, text="Run", command=self.run_algorithm, font=self.default_font, bg="skyblue", fg="black")
        self.run_button.grid(row=3, columnspan=2, padx=5, pady=10, sticky="ew")
        

        # Buttons to show algorithm information
        self.fifo_info_button = tk.Button(frame, text="FIFO Info", command=self.show_fifo_info, font=self.default_font,bg="lightgreen",fg="black")
        self.fifo_info_button.grid(row=4, column=0, padx=5, pady=5, sticky="ew")

        self.lru_info_button = tk.Button(frame, text="LRU Info", command=self.show_lru_info, font=self.default_font,bg="lightcoral",fg="black")
        self.lru_info_button.grid(row=4, column=1, padx=5, pady=5, sticky="ew")

        self.optimal_info_button = tk.Button(frame, text="Optimal Info", command=self.show_optimal_info, font=self.default_font,bg="lightyellow",fg="black")
        self.optimal_info_button.grid(row=5, column=0, padx=5, pady=5, sticky="ew")

        self.mru_info_button = tk.Button(frame, text="MRU Info", command=self.show_mru_info, font=self.default_font,bg="lightpink",fg="black")
        self.mru_info_button.grid(row=5, column=1, padx=5, pady=5, sticky="ew")

        # Canvas for frame output area
        self.canvas = tk.Canvas(frame, width=600, height=300, bg="white")
        self.canvas.grid(row=6, columnspan=2, padx=5, pady=10)

        # Variables to store statistics
        self.hit_count = 0
        self.page_fault_count = 0
        self.hit_ratio = 0
        self.miss_ratio = 0

        # Text widgets to display statistics
        self.stats_text = tk.Text(frame, width=50, height=5, font=self.default_font)
        self.stats_text.grid(row=7, columnspan=2, padx=5, pady=5)
    





    def run_algorithm(self):
        frames = self.frames_var.get()
        reference_str = self.reference_var.get()
        algorithm = self.algorithm_var.get()

        try:
            frames = int(frames)
            reference_list = list(map(int, reference_str.split(',')))

            if algorithm == "FIFO":
                self.run_fifo(frames, reference_list)
            elif algorithm == "LRU":
                self.run_lru(frames, reference_list)
            elif algorithm == "Optimal":
                self.run_optimal(frames, reference_list)
            elif algorithm == "MRU":
                self.run_mru(frames, reference_list)
            else:
                messagebox.showerror("Error", "Invalid algorithm selection.")
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter integers.")

        # Add reference cells
        self.add_reference_cells(reference_str)

    def cell(self, element, row, col):
        label = Label(self.root, text=element, padx=20, pady=10, bd=1, fg="green", relief=SOLID, anchor="center")
        label.configure(font=("Century Gothic", 12))
        label.grid(row=row, column=col)

    def animate_algorithm(self, frame_states, hits, page_faults):
        if frame_states:
            next_frame = frame_states.pop(0)
            self.update_frame_output(next_frame)
            winsound.Beep(1000, 200)  # Play a beep sound
            self.plot_graph([next_frame])  # Plot graph
            self.update_statistics(hits, page_faults)  # Update statistics
            self.root.after(500, self.animate_algorithm, frame_states, hits, page_faults)
    def update_frame_output(self, frame_state):
        for i, page in enumerate(frame_state):
            self.cell(f"Frame {page}", i + 1, 2)  # Display frame in the cell

    def run_fifo(self, frames, reference_list):
        frame_queue = []
        frame_states = []
        hits = 0
        page_faults = 0

        for page in reference_list:
            if page in frame_queue:
                hits += 1
            else:
                if len(frame_queue) == frames:
                    frame_queue.pop(0)
                frame_queue.append(page)
                page_faults += 1
            
            frame_states.append(list(frame_queue[:]))

        self.animate_algorithm(frame_states, hits, page_faults)

    def run_lru(self, frames, reference_list):
        frame_queue = []
        frame_states = []
        hits = 0
        page_faults = 0

        for page in reference_list:
            if page in frame_queue:
                frame_queue.remove(page)
                frame_queue.append(page)
                hits += 1
            else:
                if len(frame_queue) == frames:
                    frame_queue.pop(0)
                frame_queue.append(page)
                page_faults += 1
            
            frame_states.append(list(frame_queue[:]))

        self.animate_algorithm(frame_states, hits, page_faults)

    def run_optimal(self, frames, reference_list):
        frame_queue = []
        frame_states = []
        hits = 0
        page_faults = 0

        for page in reference_list:
            if page in frame_queue:
                hits += 1
            else:
                if len(frame_queue) == frames:
                    furthest_used_index = -1
                    for frame_page in frame_queue:
                        if frame_page not in reference_list[reference_list.index(page)+1:]:
                            furthest_used_index = frame_queue.index(frame_page)
                            break
                    if furthest_used_index == -1:
                        furthest_used_index = frame_queue.index(reference_list[-1])
                    frame_queue[furthest_used_index] = page
                else:
                    frame_queue.append(page)
                page_faults += 1
            
            frame_states.append(list(frame_queue[:]))

        self.animate_algorithm(frame_states, hits, page_faults)
    def run_mru(self, frames, reference_list):
        frame_queue = []
        frame_states = []
        hits = 0
        page_faults = 0

        for page in reference_list:
            if page in frame_queue:
                # If page is already in the frame, remove it and add it at the front (MRU)
                frame_queue.remove(page)
                frame_queue.insert(0, page)
                hits += 1
            else:
                if len(frame_queue) < frames:
                    # If there is space in the frame, insert the new page at the front
                    frame_queue.insert(0, page)
                else:
                    # If the frame is full, remove the MRU page (first element) and insert the new page at the front
                    frame_queue.pop(0)
                    frame_queue.insert(0, page)
                page_faults += 1
            frame_states.append(list(frame_queue[:]))

        self.animate_algorithm(frame_states, hits, page_faults)
    def update_frame_output(self, frame_state):
        self.canvas.delete("all")
        for i, page in enumerate(frame_state):
            color = self.frame_colors[i % len(self.frame_colors)]
            self.cell(page, 6, i + 2)  # Assuming the frame output starts from row 6 and column 2
    def cell(self, element, row, col):
        label = Label(self.root, text=element, padx=20, pady=10, bd=1, fg="blue", relief=SOLID, anchor="center")
        label.configure(font=("Century Gothic", 12))
        label.grid(row=row, column=col)





    def update_statistics(self, hits, page_faults):
        self.stats_text.delete(1.0, tk.END)
        self.stats_text.insert(tk.END, f"Hits: {hits}\n")
        self.stats_text.insert(tk.END, f"Page Faults: {page_faults}\n")
        self.stats_text.insert(tk.END, f"Hit Ratio: {hits / (hits + page_faults):.2f}\n")
        self.stats_text.insert(tk.END, f"Miss Ratio: {page_faults / (hits + page_faults):.2f}\n")

    def show_fifo_info(self):
        self.show_custom_info("FIFO Info", 
                      "Your FIFO algorithm description here.",
                      12,
                      path="C:\\Users\\Sneha Bansal\\OneDrive\\Desktop\\COS pbl\\image\\FifoTheory.png")

# Similar updates for other methods...



    def show_lru_info(self):
        self.show_custom_info("LRU Info", 
                      "Your LRU algorithm description here.",
                      12,
                      path="C:\\Users\\Sneha Bansal\\OneDrive\\Desktop\\COS pbl\\image\\LruTheory.png")


    def show_optimal_info(self):
        self.show_custom_info("Optimal Info", 
                      "Your Optimal algorithm description here.",
                      12,
                      path="C:\\Users\\Sneha Bansal\\OneDrive\\Desktop\\COS pbl\\image\\OptimalTheory.png")


    def show_mru_info(self):
        self.show_custom_info("MRU Info", 
                      "Your MRU algorithm description here.",
                      12,
                      path="C:\\Users\\Sneha Bansal\\OneDrive\\Desktop\\COS pbl\\image\\MruTheory.png")


    def show_custom_info(self, title, message, font_size, path=None):
        top = tk.Toplevel(self.root)
        top.title(title)

        if path:
            image = Image.open(path)
            photo = ImageTk.PhotoImage(image)
            label_image = tk.Label(top, image=photo)
            label_image.image = photo
            label_image.pack(padx=20, pady=10)

        label = tk.Label(top, text=message, font=("Arial", font_size))
        label.pack(padx=20, pady=10)

        button = tk.Button(top, text="OK", command=top.destroy)
        button.pack(pady=5)
       

    def plot_graph(self, frame_states):
        plt.figure(figsize=(4, 4))
        for i, frame_state in enumerate(frame_states):
            plt.subplot(len(frame_states), 1, i + 1)
            plt.title(f"Frame State {i+1}")
            plt.bar(range(len(frame_state)), frame_state, color=self.frame_colors[:len(frame_state)])
            plt.xlabel("Frame")
            plt.ylabel("Page")
            plt.xticks([])
            plt.yticks(range(max(frame_state) + 1))
        plt.tight_layout()
        plt.show()

    def animate_frames(self, frame_states):
        if frame_states:
            next_frame = frame_states.pop(0)
            self.update_frame_output(next_frame)
            winsound.Beep(1000, 200)  # Play a beep sound
            self.plot_graph([next_frame])  # Plot graph
            self.root.after(500, self.animate_frames, frame_states)

    def update_frame_output(self, frame_state):
        self.canvas.delete("all")
        for i, page in enumerate(frame_state):
            color = self.frame_colors[i % len(self.frame_colors)]
            x = 100
            y = 100 + i * 30
            self.canvas.create_text(x, y, anchor="w", text=f"Frame {i+1}: {page}", font=self.default_font, fill=color)
if __name__ == "__main__":
    root = tk.Tk()

    app = PageReplacementApp(root)

    root.mainloop()
