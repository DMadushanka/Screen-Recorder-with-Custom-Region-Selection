import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import threading
import pyautogui
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
import matplotlib
from tkinter import filedialog
import cv2
import numpy as np
import time

# To use a different Tk instance for the plot window
matplotlib.use("TkAgg")

class ScreenshotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Screen Recorder")

        # Initialize attributes for mouse drag
        self.start_x = None
        self.start_y = None

        # Width and Height input for custom recording size
        self.width_label = tk.Label(root, text="Enter Width for Recording:")
        self.width_label.pack()

        self.width_entry = tk.Entry(root)
        self.width_entry.pack()

        self.height_label = tk.Label(root, text="Enter Height for Recording:")
        self.height_label.pack()

        self.height_entry = tk.Entry(root)
        self.height_entry.pack()

        # Start and Stop buttons
        self.start_button = tk.Button(root, text="Start Recording", command=self.start_recording)
        self.start_button.pack()

        self.stop_button = tk.Button(root, text="Stop Recording", command=self.stop_recording)
        self.stop_button.pack()

        # Plotting the selected area
        self.plot_button = tk.Button(root, text="Draw Recording Area", command=self.show_plot)
        self.plot_button.pack()

        # Browse location button
        self.browse_button = tk.Button(root, text="Browse Save Location", command=self.browse_save_location)
        self.browse_button.pack()

        # Save location
        self.save_location = None
        self.recording = False

    def browse_save_location(self):
        # Open a file dialog to choose a directory
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.save_location = folder_selected
        else:
            self.save_location = None

    def start_recording(self):
        if self.recording:
            messagebox.showinfo("Info", "Recording is already in progress.")
            return

        # Use the selected recording region
        if hasattr(self, 'recording_region'):
            region = self.recording_region
        else:
            screen_width, screen_height = pyautogui.size()
            region = (0, 0, screen_width, screen_height)  # Default to full screen

        # Start recording in a separate thread
        self.recording = True
        threading.Thread(target=self.record_video, args=(region,)).start()

    def record_video(self, region):
        # Define video codec and output file
        fourcc = cv2.VideoWriter_fourcc(*"X264")  # Change codec to X264 for MP4
        output_path = f"{self.save_location}/recording_{int(time.time())}.mp4" if self.save_location else f"recording_{int(time.time())}.mp4"  # Change extension to .mp4
        out = cv2.VideoWriter(output_path, fourcc, 20.0, (region[2], region[3]))

        # Create a mask for rounded corners
        mask = np.zeros((region[3], region[2], 3), dtype=np.uint8)
        radius = 50  # Radius for the rounded corners
        color = (255, 255, 255)  # White color for the mask
        thickness = -1  # Fill the rectangle

        # Draw a rounded rectangle on the mask
        mask = cv2.rectangle(mask, (0, 0), (region[2], region[3]), color, thickness)
        mask = cv2.circle(mask, (radius, radius), radius, color, thickness)
        mask = cv2.circle(mask, (region[2] - radius, radius), radius, color, thickness)
        mask = cv2.circle(mask, (radius, region[3] - radius), radius, color, thickness)
        mask = cv2.circle(mask, (region[2] - radius, region[3] - radius), radius, color, thickness)

        while self.recording:
            # Capture the screen
            screenshot = pyautogui.screenshot(region=region)
            frame = cv2.cvtColor(np.array(screenshot), cv2.COLOR_BGR2RGB)

            # Apply the mask to the frame
            frame = cv2.bitwise_and(frame, mask)

            # Write the frame to the video file
            out.write(frame)

        out.release()
        messagebox.showinfo("Info", f"Recording saved to {output_path}")

    def stop_recording(self):
        if not self.recording:
            messagebox.showinfo("Info", "No recording is in progress.")
            return

        self.recording = False

    def show_plot(self):
        # Create a new Tk window for the plot
        plot_window = tk.Toplevel(self.root)
        plot_window.attributes('-fullscreen', True)  # Fullscreen
        plot_window.attributes('-alpha', 0.5)

        # Get screen dimensions
        screen_width, screen_height = pyautogui.size()

        # Create a plot to represent the screen
        fig, ax = plt.subplots()
        ax.set_xlim(0, screen_width)
        ax.set_ylim(0, screen_height)
        ax.set_title("Draw the area to record")
        ax.invert_yaxis()  # Invert y-axis to match screen coordinates

        # Set subplot configuration
        plt.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0)

        # Initialize the rectangle for the selected area
        area_rect = ax.fill([], [], 'lightgreen', label="Selected Area")[0]

        def on_press(event):
            # Capture the starting point of the rectangle
            if event.xdata and event.ydata:
                self.start_x, self.start_y = event.xdata, event.ydata

        def on_drag(event):
            # Update the rectangle dynamically as the user drags the mouse
            if event.xdata and event.ydata:
                end_x, end_y = event.xdata, event.ydata
                area_rect.set_xy([[self.start_x, self.start_y], 
                                  [end_x, self.start_y], 
                                  [end_x, end_y], 
                                  [self.start_x, end_y], 
                                  [self.start_x, self.start_y]])
                fig.canvas.draw()

        def on_enter(event):
            # Save the selected area dimensions
            if self.start_x is not None and self.start_y is not None:
                # Get the last point of the rectangle
                vertices = area_rect.get_xy()
                x1, y1 = int(vertices[0][0]), int(vertices[0][1])  # Top-left corner
                x2, y2 = int(vertices[2][0]), int(vertices[2][1])  # Bottom-right corner

                # Calculate width and height
                width, height = abs(x2 - x1), abs(y2 - y1)

                # Update the width and height entries
                self.width_entry.delete(0, tk.END)
                self.width_entry.insert(0, str(width))
                self.height_entry.delete(0, tk.END)
                self.height_entry.insert(0, str(height))

                # Save the region for recording
                self.recording_region = (min(x1, x2), min(y1, y2), width, height)

                messagebox.showinfo("Info", f"Selected area saved: X={min(x1, x2)}, Y={min(y1, y2)}, Width={width}, Height={height}")
                plot_window.destroy()

        # Connect mouse events to the plot
        fig.canvas.mpl_connect('button_press_event', on_press)
        fig.canvas.mpl_connect('motion_notify_event', on_drag)

        # Bind the "Enter" key to save the selected area
        plot_window.bind('<Return>', on_enter)

        ax.legend()

        # Embed plot in the new Tkinter window
        canvas = FigureCanvasTkAgg(fig, master=plot_window)
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        canvas.draw()

        # Add a toolbar for interaction
        toolbar = NavigationToolbar2Tk(canvas, plot_window)
        toolbar.update()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)


# Main Application
root = tk.Tk()
app = ScreenshotApp(root)
root.mainloop()
