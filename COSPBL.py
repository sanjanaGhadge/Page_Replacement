import tkinter as tk
from tkinter import messagebox
from time import sleep
import winsound
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random
from PIL import Image, ImageTk

class PageReplacementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Page Replacement")
        self.root.geometry("800x600")

        # Variables to store user input
        self.frames_var = tk.StringVar()
        self.reference_var = tk.StringVar()
        self.algorithm_var = tk.StringVar()

        # Font settings
        self.default_font = ("Arial", 14)

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
        self.info_buttons = {}
        algorithms = ["FIFO", "LRU", "Optimal", "MRU"]
        for algorithm in algorithms:
            self.info_buttons[algorithm] = tk.Button(frame, text=f"{algorithm} Info", command=lambda algo=algorithm: self.show_algorithm_info(algo), font=self.default_font, bg="lightgreen", fg="black")
            self.info_buttons[algorithm].grid(row=4+algorithms.index(algorithm), column=algorithms.index(algorithm), padx=5, pady=5, sticky="ew")

    def run_algorithm(self):
        frames = self.frames_var.get()
        reference_str = self.reference_var.get()
        algorithm = self.algorithm_var.get()

        try:
            frames = int(frames)
            reference_list = list(map(int, reference_str.split(',')))

            if algorithm == "FIFO":
                self.animate_fifo(frames, reference_list)
            elif algorithm == "LRU":
                self.animate_lru(frames, reference_list)
            elif algorithm == "Optimal":
                self.animate_optimal(frames, reference_list)
            elif algorithm == "MRU":
                self.animate_mru(frames, reference_list)
            else:
                messagebox.showerror("Error", "Invalid algorithm selection.")
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter integers.")

    def animate_fifo(self, frames, reference_list):
        frame_queue = []
        page_faults = 0
        hits = 0
        frame_states = []

        for page in reference_list:
            if page in frame_queue:
                hits += 1
            else:
                if len(frame_queue) == frames:
                    frame_queue.pop(0)
                frame_queue.append(page)
                page_faults += 1
            
            frame_states.append(list(frame_queue))

        self.animate_output(frame_states, page_faults, hits, len(reference_list))

    def animate_lru(self, frames, reference_list):
        frame_queue = []
        page_faults = 0
        hits = 0
        frame_states = []

        for page in reference_list:
            if page in frame_queue:
                hits += 1
                frame_queue.remove(page)
            else:
                if len(frame_queue) == frames:
                    frame_queue.pop(0)
                page_faults += 1
            
            frame_queue.append(page)
            frame_states.append(list(frame_queue))

        self.animate_output(frame_states, page_faults, hits, len(reference_list))
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
                    page_faults += 1
                else:
                    frame_queue.append(page)
                    page_faults += 1
            frame_states.append(list(frame_queue[:]))
            self.animate_output(frame_states, page_faults, hits, len(reference_list))
        



    def animate_mru(self, frames, reference_list):
        frame_queue = []
        page_faults = 0
        hits = 0
        frame_states = []
        for page in reference_list:
            if page in frame_queue:
                hits += 1
            else:
                if len(frame_queue) == frames:
                    frame_queue.pop(0)
                    page_faults += 1
            frame_queue.insert(0, page)
            page_faults += 1
        frame_states.append(list(frame_queue))

        self.animate_output(frame_states, page_faults, hits, len(reference_list))



    

    def animate_output(self, frame_states, page_faults, hits, total_pages):
        for state in frame_states:
            self.update_frame_output(state)
            self.root.update()  # Update the GUI
            winsound.Beep(1000, 200)  # Play a beep sound
            sleep(1)  # Pause for visualization

        # After animation is done, display graph and statistics
        self.plot_graph(frame_states)
        hit_rate = hits / total_pages
        miss_rate = page_faults / total_pages
        self.show_custom_info("Result", f"Page Faults: {page_faults}\nHits: {hits}\nHit Rate: {hit_rate:.2f}\nMiss Rate: {miss_rate:.2f}", 16)

    def update_frame_output(self, frame_state):
        # Clear previous content
        for widget in self.root.winfo_children():
            widget.destroy()

        # Display frames in a table-like format with random background colors
        for i, page in enumerate(frame_state):
            bg_color = "#{:06x}".format(random.randint(0, 0xFFFFFF))  # Random color
            label = tk.Label(self.root, text=f"Frame {i+1}: {page if page else 'Empty'}", font=("Arial", 14), bg=bg_color)
            label.grid(row=i+1, column=0, padx=10, pady=5, sticky="nsew")

    def plot_graph(self, frame_states):
        # Clear previous content
        for widget in self.root.winfo_children():
            widget.destroy()

        fig, ax = plt.subplots(figsize=(6, 4))

        for i, state in enumerate(frame_states):
            ax.plot(range(len(state)), state, label=f"Frame {i+1}")

        ax.set_xlabel("Time")
        ax.set_ylabel("Page")
        ax.legend()
        ax.grid(True)

        canvas = FigureCanvasTkAgg(fig, master=self.root)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=0, padx=10, pady=5)
        self.info_images = {}
        
    def show_algorithm_info(self, algorithm):
        if algorithm == "FIFO":
            self.show_fifo_info()
        elif algorithm == "LRU":
            self.show_lru_info()
        elif algorithm == "Optimal":
            self.show_optimal_info()
        elif algorithm == "MRU":
            self.show_mru_info()

    def show_fifo_info(self):
        self.show_custom_info("FIFO Info", 
                      "Your FIFO algorithm description here.",
                      12,
                      path="C:\\Users\\Sneha Bansal\\OneDrive\\Desktop\\COS pbl\\image\\FifoTheory.png")

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
            label_image.image = photo  # Keep a reference to the image
            label_image.pack(padx=20, pady=10)

        label = tk.Label(top, text=message, font=("Arial", font_size))
        label.pack(padx=20, pady=10)

        button = tk.Button(top, text="OK", command=top.destroy)
        button.pack(pady=5)

if __name__ == "__main__":
    root = tk.Tk()
    app = PageReplacementApp(root)
    root.mainloop()
