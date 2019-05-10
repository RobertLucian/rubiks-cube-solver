# import asyncio
# import json
# import arms
# import kociemba

# # to calibrate the arms 
# # and report the identified colors 
# # along with the captured images
# async def configurator():
#     pass

# # to manipulate/solve/stop the actual cube
# async def runner():
#     pass

# # to broadcast the camera feed
# async def camera():
#     pass

# # to collect the images for each face of the cube
# def image_collector():
#     pass

# # to detect the colors on each face
# def image_processor():
#     pass

# # to solve the cube with the Kociemba algorithm
# def rubik_solver():
#     pass

# # to convert the output from the solver to 
# # what the arm generator needs
# def solver_converter():
#     pass

# # to convert the generated solution
# # to whatever the arms need
# def arm_generator():
#     pass

# # to apply the solution onto the real-world cube
# def cube_executor():
#     pass

from tkinter import ttk
from queue import Queue
from PIL import ImageTk, Image

import tkinter as tk
import threading as td
import picamera
import io

# generic page that can be brought onto the front plane
class Page(tk.Frame):
    def __init__(self, *args, **kwargs):
        super(Page, self).__init__(*args, **kwargs)
        self.place(x=0, y=0, relwidth=1.0, relheight=1.0)

    def show(self):
        self.lift()

class Solver(Page):
    def __init__(self, *args, **kwargs):
        super(Solver, self).__init__(*args, **kwargs)

        # Grip/Stop Functions
        self.grip_labelframe = tk.LabelFrame(self, text='Grip/Stop Functions')
        self.grip_labelframe.pack(side='left', fill=tk.Y, ipadx=2, ipady=2, padx=20, pady=20)

        # Side Grip/Stop Buttons
        self.button_names = ['Fix', 'Release', 'Stop', 'Cut Power']
        max_button_width = max(map(lambda x: len(x), self.button_names))
        self.buttons = {}
        for button_name in self.button_names:
            self.buttons[button_name] = tk.Button(self.grip_labelframe, text=button_name, width=max_button_width, height=1, command=lambda label=button_name: self.button_action(label))
            self.buttons[button_name].pack(side='top', expand=True)

        # Solver/Reader Functions
        self.solver_labelframe = tk.LabelFrame(self, text='Solver/Reader Functions')
        self.solver_labelframe.pack(side='left', fill=tk.BOTH, ipadx=2, ipady=2, padx=20, pady=20, expand=True)

        # Solver/Reader Buttons & Progress Bars 

        self.solver_labelframe.rowconfigure(0, weight=1)
        self.solver_labelframe.rowconfigure(1, weight=1)
        self.solver_labelframe.columnconfigure(0, weight=1)
        self.solver_labelframe.columnconfigure(1, weight=3)
        self.solver_labelframe.columnconfigure(2, weight=1)

        new_buttons = ['Read Cube', 'Solve Cube']
        max_button_width = max(map(lambda x: len(x), new_buttons))
        for idx, button_name in enumerate(new_buttons):
            self.buttons[button_name] = tk.Button(self.solver_labelframe, text=button_name, width=max_button_width, height=1, command=lambda label=button_name: self.button_action(label))
            self.buttons[button_name].grid(row=idx, column=0, padx=20, pady=20, sticky='nw')

        self.progress_bars = {}
        self.bar_names = new_buttons
        for idx, bar_name in enumerate(self.bar_names):
            self.progress_bars[bar_name] = ttk.Progressbar(self.solver_labelframe, orient='horizontal', length=100, mode='determinate')
            self.progress_bars[bar_name].grid(row=idx, column=1, padx=20, pady=20, sticky='nwe')

        self.progress_labels = {}
        self.label_names = new_buttons
        max_button_width = max(map(lambda x: len(x), self.label_names))
        for idx, label_name in enumerate(self.label_names):
            self.progress_labels[label_name] = tk.Label(self.solver_labelframe, text='n/a', height=1, width=max_button_width, justify=tk.LEFT, anchor=tk.W)
            self.progress_labels[label_name].grid(row=idx, column=2, padx=20, pady=20, sticky='nw')

        self.button_names += new_buttons
        self.buttons['Solve Cube'].config(state='disabled')

    def button_action(self, label):
        print(label)

class Camera(Page):
    def __init__(self, *args, **kwargs):
        super(Camera, self).__init__(*args, **kwargs)

        # left big frame
        self.entries_frame = tk.LabelFrame(self, text='Interest Zones')
        self.entries_frame.pack(side='left', fill=tk.Y, ipadx=2, ipady=2, padx=20, pady=20)

        # configure layout of labels and buttons in the left frame
        self.entries_frame.rowconfigure(0, weight=1)
        self.entries_frame.rowconfigure(1, weight=1)
        self.entries_frame.rowconfigure(2, weight=1)
        self.entries_frame.rowconfigure(3, weight=1)
        self.entries_frame.rowconfigure(4, weight=1)
        self.entries_frame.columnconfigure(0, weight=1)
        self.entries_frame.columnconfigure(1, weight=1)

        # and setup the labels and the buttons in the left frame
        self.labels = {}
        self.entries = {}
        self.entry_values = {}
        self.label_names = ['X Offset (px)', 'Y Offset (px)', 'Size (px)', 'Pad (px)']
        max_button_width = max(map(lambda x: len(x), self.label_names))
        for idx, text in enumerate(self.label_names):
            self.labels[text] = tk.Label(self.entries_frame, text=text, height=1, width=max_button_width, justify='right', anchor=tk.W)
            self.labels[text].grid(row=idx, column=0, padx=20, pady=10)

            self.entry_values[text] = tk.IntVar()
            self.entries[text] = tk.Entry(self.entries_frame, justify='left', width=5, textvariable=self.entry_values[text])
            self.entries[text].grid(row=idx, column=1, padx=20, pady=10)

        # create the capture button
        self.capture_button = tk.Button(self.entries_frame, text='Get Preview', command=self.button_pressed)
        self.capture_button.grid(row=4, column=0, columnspan=2)

        # right big frame (actually label) that includes the preview image from the camera
        self.images = tk.Label(self, text='No captured image', bd=2, relief=tk.RIDGE)
        self.images.pack(side='left', fill=tk.BOTH, ipadx=2, ipady=2, padx=20, pady=20, expand=True)

    
    # every time the get preview button is pressed
    def button_pressed(self):
        for entry in self.label_names:
            self.entry_values[entry].get()

        img = ImageTk.PhotoImage(camera.capture())
        self.images.configure(image=img)
        self.images.image = img


class Arms(Page):
    def __init__(self, *args, **kwargs):
        super(Arms, self).__init__(*args, **kwargs)
        label = tk.Label(self, text="This is page arms", bg='green', justify=tk.CENTER)
        label.pack(side="top", fill="both", expand=True)

class MainView(tk.Tk):
    def __init__(self, size, name, queues):

        # initialize root window and shit
        super(MainView, self).__init__()
        self.geometry(size)
        self.title(name)
        self.resizable(False, False)
        self.queues = queues
        # initialize master-root window
        window = tk.Frame(self, bd=2)
        window.pack(side='top', fill=tk.BOTH, expand=True)
        
        # create the 2 frames within the window container
        button_navigator = tk.Frame(window, bd=2, relief=tk.FLAT)
        pages = tk.Frame(window, bd=2, relief=tk.RIDGE)

        # define the frames' dimensions
        window.rowconfigure(0, weight=19)
        window.rowconfigure(1, weight=1, minsize=25)
        window.columnconfigure(0, weight=1)

        # and organize them by rows/columns
        pages.grid(row=0, column=0, sticky="nswe", padx=2, pady=2)
        button_navigator.grid(row=1, column=0, sticky="nswe", padx=2, pady=2)

        # create the 3 pages 
        self.frames = {}
        for F in (Solver, Camera, Arms):
            page_name = F.__name__
            frame = F(pages)
            self.frames[page_name] = frame

        # and link the pages to their respective buttons
        for label in ("Solver", "Camera", "Arms"):
            button = tk.Button(button_navigator, text=label, command=self.frames[label].show)
            button.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=3)

        # and show the default page
        self.frames['Solver'].show()

class PiCameraPhotos():
    def __init__(self):
        # initialize camera with a set of predefined values
        self.camera = picamera.PiCamera()
        self.resolution = (1920, 1080)
        self.framerate = 30
        self.sensor_mode = 1
        self.rotation = 0
        self.shutter_speed = 1000.0 / self.framerate
        self.brightness = 50
        self.awb_mode = "off"
        self.awb_gains = 1.5
        
        # also initialize the container for the image
        self.stream = io.BytesIO() 

    def capture(self):
        self.stream.seek(0)
        self.camera.capture(self.stream, use_video_port=True, resize=(640, 480), format='jpeg')
        self.stream.seek(0)
        return Image.open(self.stream)

if __name__ == "__main__":
    camera = PiCameraPhotos()

    app = MainView(size="800x400", name="Rubik's Solver", queues=2)
    app.mainloop()

    # camera = PiCameraPhotos()
    # image = camera.capture()