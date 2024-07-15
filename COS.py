import tkinter as tk
from pygame import mixer
import time

class PageReplacementAlgorithm:
    def __init__(self, capacity):
        self.capacity = capacity
        self.pages = []
        self.hit_count = 0
        self.miss_count = 0

    def page_fault(self, page):
        if page in self.pages:
            self.hit_count += 1
            return False
        else:
            self.miss_count += 1
            if len(self.pages) == self.capacity:
                self.evict_page()
            self.pages.append(page)
            return True

    def hit_ratio(self):
        if self.hit_count + self.miss_count == 0:
            return 0
        return self.hit_count / (self.hit_count + self.miss_count)

    def miss_ratio(self):
        if self.hit_count + self.miss_count == 0:
            return 0
        return self.miss_count / (self.hit_count + self.miss_count)

    def evict_page(self):
        raise NotImplementedError("Subclasses must implement evict_page method")

class FIFO(PageReplacementAlgorithm):
    def evict_page(self):
        self.pages.pop(0)

class LRU(PageReplacementAlgorithm):
    def evict_page(self):
        self.pages.pop(self.pages.index(self.pages[0]))

class Optimal(PageReplacementAlgorithm):
    def evict_page(self):
        page_to_evict = max(self.pages, key=lambda p: self.pages.index(p))
        self.pages.remove(page_to_evict)

class MRU(PageReplacementAlgorithm):
    def evict_page(self):
        self.pages.pop()

def simulate(pages_reference, capacity, frame_width, frame_height, algorithm):
    page_replacement_algorithm = algorithm(capacity)

    root = tk.Tk()
    root.title(f"Page Replacement Simulation - {algorithm.__name__}")

    canvas = tk.Canvas(root, width=600, height=400)
    canvas.pack()

    text = canvas.create_text(300, 50, text="", font=("Arial", 14))

    mixer.init()  # Initialize mixer outside the loop

    frame_start_x = 50
    frame_start_y = 100
    frame_spacing = 20

    def draw_frames(replaced_page=None):
        canvas.delete("frame")
        for i, page in enumerate(page_replacement_algorithm.pages):  # Iterate over pages
            x = frame_start_x
            y = frame_start_y + i * (frame_height + frame_spacing)
            color = "light gray"
            if replaced_page is not None and i == replaced_page:
                color = "red"
            canvas.create_rectangle(x, y, x + frame_width, y + frame_height, fill=color, outline="black", tags="frame")
            canvas.create_text(x + frame_width/2, y + frame_height/2, text=str(page), fill="black", font=("Arial", 12))

    def animate(index=0):
        if index < len(pages_reference):
            page = pages_reference[index]
            replaced_page = None
            if page_replacement_algorithm.page_fault(page):
                message = f"Page fault occurred for page {page} - MISS\nHits: {page_replacement_algorithm.hit_count}, Page Faults: {page_replacement_algorithm.miss_count}\nHit Ratio: {page_replacement_algorithm.hit_ratio():.2f}, Miss Ratio: {page_replacement_algorithm.miss_ratio():.2f}"
                mixer.music.load('C:\\Users\\Sneha Bansal\\OneDrive\\Desktop\\COS pbl\\bleep-41488.mp3')
                mixer.music.play()
            else:
                message = f"Page {page} is already in memory - HIT\nHits: {page_replacement_algorithm.hit_count}, Page Faults: {page_replacement_algorithm.miss_count}\nHit Ratio: {page_replacement_algorithm.hit_ratio():.2f}, Miss Ratio: {page_replacement_algorithm.miss_ratio():.2f}"
            canvas.itemconfig(text, text=message)
            draw_frames(replaced_page)
            root.update()
            time.sleep(1)
            root.after(1000, animate, index + 1)  # Schedule next iteration after 1000ms (1 second)

    animate_button = tk.Button(root, text="Start Simulation", command=animate)
    animate_button.pack()

    root.mainloop()

# User input for frame size and capacity
frame_width = int(input("Enter frame width: "))
frame_height = int(input("Enter frame height: "))
capacity = int(input("Enter capacity: "))

# User input for page reference string
pages_reference_string = input("Enter page reference string (e.g., 1 3 0 3 5 6 3): ")
pages_reference = list(map(int, pages_reference_string.split()))

# Start simulation with different algorithms
simulate(pages_reference, capacity, frame_width, frame_height, FIFO)
simulate(pages_reference, capacity, frame_width, frame_height, LRU)
simulate(pages_reference, capacity, frame_width, frame_height, Optimal)
simulate(pages_reference, capacity, frame_width, frame_height, MRU)
