
# Importamos las librerías necesarias
from pathlib import Path
from PIL import Image as Pil_image, ImageTk as Pil_imageTk
from tkinter import ttk
import tkinter as tk
import cv2

global cameras_list

# Definimos las cámaras a utilizar
camerasLevel = [(0, 1), (2, 3), (4, 5)]
config_path = Path('config.txt')

nivel_actual = 1

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
        update_cameras(nivel_actual, '', tk.Label())

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
            combos_camera_config.append(ttk.Combobox(row_frame, values=[f"Camera {i+1}" for i in range(6)]))
            combos_camera_config[-1].current(camerasLevel[i][j])
            combos_camera_config[-1].pack(side=tk.LEFT, padx=5, pady=10)

    # Add a button for saving the configuration
    save_button = tk.Button(config_window, text="Save Configuration", command=save_config)
    save_button.pack(side=tk.BOTTOM, padx=5, pady=10)

def update_cameras(index, button_text,label):
    """Actualiza los frames de video con las nuevas cámaras."""
    global camera1, camera2, camera_frame1, camera_frame2, nivel_actual

    nivel_actual=index
    camera1.release()
    camera2.release()

    #camera1 = cv2.VideoCapture(cameras_list[index])
    #camera2 = cv2.VideoCapture(cameras_list[(index+1) % len(cameras_list)])

    camera1 = cv2.VideoCapture(cameras_list[camerasLevel[index][0]])
    camera2 = cv2.VideoCapture(cameras_list[camerasLevel[index][1]])

    update_video(camera1, camera_frame1)
    update_video(camera2, camera_frame2)
    
    label.config(text=f"Nivel {index+1}")

    # Actualizar el frame principal
    root.update()

def update_video(cap, canvas):
    # Continuar leyendo frames mientras la ventana esté abierta
    if root.winfo_exists():
        ret, frame = cap.read()
        if ret:
            # Cambiar tamaño del frame para que encaje en el canvas
            width, height = canvas.winfo_width(), canvas.winfo_height()
            frame = cv2.resize(frame, (width, height))

            # Convertir el frame a RGB y crear un PhotoImage
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            photo = Pil_imageTk.PhotoImage(Pil_image.fromarray(frame))

            # Actualizar el canvas con la nueva imagen
            canvas.create_image(0, 0, image=photo, anchor=tk.NW)
            canvas.photo = photo  

        # Programar la próxima actualización después de un corto retraso
        root.after(50, update_video, cap, canvas)

def main():
    global root, camera1, camera2, camera_frame1, camera_frame2

    # Crear la ventana principal
    root = tk.Tk()
    root.geometry("1000x600")
    root.title("Interfaz de Video")

    def on_window_config(event: tk.Event) -> None:
        """Actualizar tamaño de los frames de video y botones al cambiar el tamaño de la ventana."""
        width, height = root.winfo_width()-60, root.winfo_height()-60
        video_width, video_height = width // 2, height*7 // 9
        camera_frame1.config(width=video_width, height=video_height)
        camera_frame2.config(width=video_width, height=video_height)
        """
        level_buttons_frame_width = tk.PhotoImage(width=1, height=1)
        level_buttons_frame_height = height // 3
        level_buttons_frame.config(width=level_buttons_frame_width.width(), height=level_buttons_frame_height)

        button_width = video_width // 3
        button_height = level_buttons_frame_height // 3
        for i, button in enumerate(level_buttons_frame.winfo_children()[:3]):
            button.place(x=i*button_width + 10*i, y=0, width=button_width, height=button_height)

        print(width, video_width, button_width)
        config_button.place(x=button_width*5+20, width=button_width, height=button_height)
        """
    root.bind("<Configure>", on_window_config)

    # Crear un frame principal
    frame = tk.Frame(root)
    frame.pack(padx=20, pady=20)

    # Agregar un label al frame
    label = tk.Label(frame, text="Nivel "+ str(nivel_actual), font=("Helvetica", 24))
    label.pack()

    # Definir acciones para cada botón
    button_actions = [lambda index=i, text=f"Nivel {i+1}": update_cameras(index, text, label) for i in range(3)]

    # Agregar botones al frame
    buttons_frame = tk.Frame(root)
    buttons_frame.pack(side=tk.TOP, pady=20)

    button_reports = tk.Button(buttons_frame, text="Módulo de Reportes", command=lambda: print("Presionaste el botón Módulo de Reportes"), bg="#4CAF50", fg="white", font=("Helvetica", 14))
    button_reports.pack(side=tk.LEFT, padx=20)

    button_reports2 = tk.Label(buttons_frame ,text="         ", font=("Helvetica", 24))
    button_reports2.pack(side=tk.LEFT, padx=0)

    for i, action in enumerate(button_actions):
        button = tk.Button(buttons_frame, text=f"Nivel {i+1}", command=action, bg="#4CAF50", fg="white", font=("Helvetica", 14))
        button.pack(side=tk.LEFT, padx=20)

    # Crear botones adicionales



    button_config = tk.Button(buttons_frame, text="Configuración", command=open_config, bg="#4CAF50", fg="white", font=("Helvetica", 14))
    button_config.pack(side=tk.RIGHT, padx=20)
    button_reports2 = tk.Label(buttons_frame ,text="          ", font=("Helvetica", 24))
    button_reports2.pack(side=tk.RIGHT, padx=20)

    # Crear frames internos para los videos
    camera_frame1 = tk.Canvas(frame, width=300, height=300, bg="gray")
    camera_frame1.pack(side=tk.LEFT, padx=(0, 10))

    camera_frame2 = tk.Canvas(frame, width=300, height=300, bg="gray")
    camera_frame2.pack(side=tk.LEFT, padx=(10, 0))

    camera1 = cv2.VideoCapture(cameras_list[camerasLevel[0][0]])
    camera2 = cv2.VideoCapture(cameras_list[camerasLevel[0][1]])

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
    cameras_list = list_cameras()
    if not cameras_list:
        print("No se encontraron cámaras.")
    load_config()
    main()



   
