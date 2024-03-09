from pathlib import Path
from PIL import Image as Pil_image, ImageTk as Pil_imageTk
from tkinter import ttk
import tkinter as tk
import cv2

camerasLevel = [[0, 1], [2, 3], [4, 5]]
config_path = Path('config.txt')

def open_config():
    def save_config():
        # Logic to save the selected camera configuration
        print("Configuration saved")
        with open(config_path, 'w') as file:
            for i in range(3):
                for j in range(2):
                    camerasLevel[i][j] = combos_camera_config[i*2+j].current()
                    file.write(f"{camerasLevel[i][j]} ")
                file.write("\n")
        config_window.destroy()
        update_cameras([], 0)

    config_window = tk.Toplevel(root)
    config_window.title("Camera Configuration")
    config_window.grab_set()
    combos_camera_config = []

    # Create a grid layout with 3 rows and 3 columns
    for i in range(3):
        row_frame = tk.Frame(config_window)
        row_frame.pack(fill=tk.X)
        level = tk.Label(row_frame, text=f"Nivel {i+1}")
        level.pack(side=tk.LEFT, padx=5, pady=10)
        for j in range(2):
            #combo = ttk.Combobox(row_frame, values=[f"Camera {i}" for i in cameras])
            combos_camera_config.append(ttk.Combobox(row_frame, values=[f"Camera {i}" for i in range(6)]))
            combos_camera_config[-1].current(camerasLevel[i][j])
            combos_camera_config[-1].pack(side=tk.LEFT, padx=5, pady=10)

    # Add a button for saving the configuration
    save_button = tk.Button(config_window, text="Save Configuration", command=save_config)
    save_button.pack(side=tk.BOTTOM, padx=5, pady=10)

def select_camera(index):
    print(f"Selected camera: {cameras[index]}")


def update_cameras(cameras_list, index):
    """Update the video frames with the new cameras."""
    global camera1, camera2, camera_frame1, camera_frame2

    camera1.release()
    camera2.release()

    #camera1 = cv2.VideoCapture(cameras_list[index])
    #camera2 = cv2.VideoCapture(cameras_list[(index+1) % len(cameras_list)])

    #With Levels
    camera1 = cv2.VideoCapture(camerasLevel[index][0])
    camera2 = cv2.VideoCapture(camerasLevel[index][1])

    update_video(camera1, camera_frame1)
    update_video(camera2, camera_frame2)

def update_video(cap, canvas):
    # Continue reading frames while window is open
    if root.winfo_exists():
        ret, frame = cap.read()
        if ret:
            # Resize frame to fit the canvas
            width, height = canvas.winfo_width(), canvas.winfo_height()
            frame = cv2.resize(frame, (width, height))

            # Convert frame to RGB and create PhotoImage
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            photo = Pil_imageTk.PhotoImage(Pil_image.fromarray(frame))

            # Update the canvas with the new image
            canvas.create_image(0, 0, image=photo, anchor=tk.NW)
            canvas.photo = photo  # Keep a reference for garbage collection

        # Schedule next update after a short delay
        root.after(50, update_video, cap, canvas)

def main(cameras_list):
    global root, camera1, camera2, camera_frame1, camera_frame2

    # Create the main window
    root = tk.Tk()
    root.geometry("1000x600")
    root.title("Frame with Buttons and Video Frames")

    def on_window_config(event: tk.Event) -> None:
        """Update video frame and button sizes when the window is resized."""
        width, height = root.winfo_width()-60, root.winfo_height()-60
        video_width, video_height = width // 2, height*7 // 9
        camera_frame1.config(width=video_width, height=video_height)
        camera_frame2.config(width=video_width, height=video_height)

        level_buttons_frame_width = tk.PhotoImage(width=1, height=1)
        level_buttons_frame_height = height // 3
        level_buttons_frame.config(width=level_buttons_frame_width.width(), height=level_buttons_frame_height)

        button_width = video_width // 3
        button_height = level_buttons_frame_height // 3
        for i, button in enumerate(level_buttons_frame.winfo_children()[:3]):
            button.place(x=i*button_width + 10*i, y=0, width=button_width, height=button_height)

        print(width, video_width, button_width)
        config_button.place(x=button_width*5+20, width=button_width, height=button_height)

    root.bind("<Configure>", on_window_config)

    # Create a frame
    frame = tk.Frame(root)
    frame.pack(padx=20, pady=20)  # Add some padding around the frame

    # Add a label to the frame
    label = tk.Label(frame, text="OSO")
    label.pack()

    # Define actions for each button
    button_actions = [lambda index=i: update_cameras(cameras_list, index) for i in range(3)]

    # Create internal frames for videos
    cameras_frame = tk.Frame(frame)
    cameras_frame.pack(side=tk.TOP, fill=tk.X, expand=True)

    camera_frame1 = tk.Canvas(cameras_frame, width=300, height=300, bg="gray")
    camera_frame1.pack(side=tk.LEFT, padx=(0, 10))

    camera_frame2 = tk.Canvas(cameras_frame, width=300, height=300, bg="gray")
    camera_frame2.pack(side=tk.LEFT, padx=(10, 0))

    # Add buttons to the frame
    level_buttons_frame = tk.Frame(root)
    level_buttons_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=20, pady=20)

    # Create two buttons with different actions
    for i in range(0, 3):
        button = tk.Button(level_buttons_frame, text=f"Button {i+1}", command=button_actions[i])
        button.pack(side=tk.LEFT, padx=(0, 10))

    config_button = tk.Button(level_buttons_frame, text="Config", command=open_config)
    config_button.pack(side=tk.RIGHT, padx=(0, 10))

    camera1 = cv2.VideoCapture(cameras_list[0])
    camera2 = cv2.VideoCapture(cameras_list[1])

    update_video(camera1, camera_frame1)
    update_video(camera2, camera_frame2)

    root.mainloop()

def list_cameras():
    cameras = []
    for i in range(cv2.CAP_DSHOW, cv2.CAP_DSHOW + 10):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            cameras.append(i)
            cap.release()
    return cameras

def load_config():
    if not config_path.is_file(): return
    with open(config_path, 'r') as file:
        for i in range(3):
            level_config = file.readline().split(' ')
            camerasLevel[i] = [int(level_config[0]), int(level_config[1])]

if __name__ == '__main__':
    cameras = list_cameras()
    if not cameras:
        print("No cameras found.")
    load_config()
    main(cameras)