
from tkinter import *
import pyttsx3


def one():
    text = "FIFO IS SELECTED"
    engine.say(text)
    engine.runAndWait()

    photo_root = Toplevel()
    photo_root.title("FIFO Theory")
    photo_root.geometry("1152x648")
    photo_root.resizable(False, False)
    photo = PhotoImage(file="image\FifoTheory.png")
    photo_label = Label(photo_root, image=photo)
    photo_label.pack()
    photo_root.mainloop()


def two():
    text = "LIFO IS SELECTED"
    engine.say(text)
    engine.runAndWait()

    photo_root = Toplevel()
    photo_root.title("LIFO Theory")
    photo_root.geometry("1152x648")
    photo_root.resizable(False, False)
    photo = PhotoImage(file="C:\\Users\\Sneha Bansal\\OneDrive\\Desktop\\COS pbl\\image\\LifoTheory.png")
    photo_label = Label(photo_root, image=photo)
    photo_label.pack()
    photo_root.mainloop()


def three():
    text = "LRU IS SELECTED"
    engine.say(text)
    engine.runAndWait()

    photo_root = Toplevel()
    photo_root.title("LRU Theory")
    photo_root.geometry("1152x648")
    photo_root.resizable(False, False)
    photo = PhotoImage(file="C:\\Users\\Sneha Bansal\\OneDrive\\Desktop\\COS pbl\\image\\LruTheory.png")
    photo_label = Label(photo_root, image=photo)
    photo_label.pack()
    photo_root.mainloop()


def four():
    text = "MRU IS SELECTED"
    engine.say(text)
    engine.runAndWait()

    photo_root = Toplevel()
    photo_root.title("MRU Theory")
    photo_root.geometry("1152x648")
    photo_root.resizable(False, False)
    photo = PhotoImage(file="C:\\Users\\Sneha Bansal\\OneDrive\\Desktop\\COS pbl\\image\\MruTheory.png")
    photo_label = Label(photo_root, image=photo)
    photo_label.pack()
    photo_root.mainloop()


def five():
    text = "Optimal IS SELECTED"
    engine.say(text)
    engine.runAndWait()

    photo_root = Toplevel()
    photo_root.title("Optimal Theory")
    photo_root.geometry("1152x648")
    photo_root.resizable(False, False)
    photo = PhotoImage(file="C:\\Users\\Sneha Bansal\\OneDrive\\Desktop\\COS pbl\\image\\OptimalTheory.png")
    photo_label = Label(photo_root, image=photo)
    photo_label.pack()
    photo_root.mainloop()


def six():
    text = "Random IS SELECTED"
    engine.say(text)
    engine.runAndWait()

    photo_root = Toplevel()
    photo_root.title("Random Theory")
    photo_root.geometry("1152x648")
    photo_root.resizable(False, False)
    photo = PhotoImage(file="C:\\Users\\Sneha Bansal\\OneDrive\\Desktop\\COS pbl\\image\\RandomTheory.png")
    photo_label = Label(photo_root, image=photo)
    photo_label.pack()
    photo_root.mainloop()

engine = pyttsx3.init()
# -----------------------------------------------------------------------------------------------------------------------
# Home Page
Menu = Tk()

Menu.title("Theory Of PRA")
Menu.overrideredirect(False)
Menu.geometry("800x750+0+0")
Menu.resizable(False, False)

L1 = Label(bg="black", text="Theory Of PRA", fg="white", font=("Century Gothic", 35), width="900",
           height="1")
L1.pack()
f1 = Frame(bg="white").pack()
l1 = Label(text="Choose Theory: ", font=("Century Gothic", 15))
l1.pack(pady="40")
Button1 = Button(f1, text="First In First Out", borderwidth="0", bg="#e8e8e8", fg="green", font=("Century Gothic", 18),
                 activeforeground="black", activebackground="#bbbfca", command=one).pack()
Button2 = Button(f1, text="Last In First Out", borderwidth="0", bg="#e8e8e8", fg="green", font=("Century Gothic", 18),
                 activeforeground="black", activebackground="#bbbfca", command=two).pack(pady="30")
Button3 = Button(f1, text="Least Recently Used", borderwidth="0", bg="#e8e8e8", fg="green", font=("Century Gothic", 18),
                 activeforeground="black", activebackground="#bbbfca", command=three).pack()
Button4 = Button(f1, text="Most Recently Used", borderwidth="0", bg="#e8e8e8", fg="green", font=("Century Gothic", 18),
                 activeforeground="black", activebackground="#bbbfca", command=four).pack(pady="30")
Button5 = Button(f1, text="Optimal PRA", borderwidth="0", bg="#e8e8e8", fg="green", font=("Century Gothic", 18),
                 activeforeground="black", activebackground="#bbbfca", command=five).pack()
Button6 = Button(f1, text="Random PRA", borderwidth="0", bg="#e8e8e8", fg="green", font=("Century Gothic", 18),
                 activeforeground="black", activebackground="#bbbfca", command=six).pack(pady="30")
Button7 = Button(f1, text="Back", borderwidth="0", bg="#e8e8e8", fg="green", font=("Century Gothic", 18),
                 activeforeground="black", activebackground="#bbbfca", command=Menu.destroy).pack()
Menu.mainloop()
