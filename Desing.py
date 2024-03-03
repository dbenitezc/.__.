
# Importamos las librerías necesarias
from PIL import Image as Pil_image, ImageTk as Pil_imageTk
import tkinter as tk
import cv2

# Definimos las cámaras a utilizar
camerasLevel = [(0, 1), (2, 3), (4, 5)]

nivel_actual = 1

def update_cameras(cameras_list, index, button_text,label):
    """Actualiza los frames de video con las nuevas cámaras."""
    global camera1, camera2, camera_frame1, camera_frame2, nivel_actual

    nivel_actual=f"Nivel {index+1}"
    camera1.release()
    camera2.release()

    camera1 = cv2.VideoCapture(cameras_list[index])
    camera2 = cv2.VideoCapture(cameras_list[(index+1) % len(cameras_list)])

    update_video(camera1, camera_frame1)
    update_video(camera2, camera_frame2)
    
    label.config(text=nivel_actual)

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

def main(cameras_list):
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

    root.bind("<Configure>", on_window_config)

    # Crear un frame principal
    frame = tk.Frame(root)
    frame.pack(padx=20, pady=20)

    # Agregar un label al frame
    label = tk.Label(frame, text="Nivel "+ str(nivel_actual), font=("Helvetica", 24))
    label.pack()

    # Definir acciones para cada botón
    button_actions = [lambda index=i, text=f"Nivel {i+1}": update_cameras(cameras_list, index, text, label) for i in range(3)]

    # Agregar botones al frame
    buttons_frame = tk.Frame(root)
    buttons_frame.pack(side=tk.TOP, pady=20)

    for i, action in enumerate(button_actions):
        button = tk.Button(buttons_frame, text=f"Nivel {i+1}", command=action, bg="#4CAF50", fg="white", font=("Helvetica", 14))
        button.pack(side=tk.LEFT, padx=20)

    # Crear botones adicionales
    button_reports = tk.Button(buttons_frame, text="Módulo de Reportes", command=lambda: print("Presionaste el botón Módulo de Reportes"), bg="#4CAF50", fg="white", font=("Helvetica", 14))
    button_reports.pack(side=tk.LEFT, padx=20)
    

    button_config = tk.Button(buttons_frame, text="Configuración", command=lambda: print("Presionaste el botón Configuración"), bg="#4CAF50", fg="white", font=("Helvetica", 14))
    button_config.pack(side=tk.RIGHT, padx=20)

    # Crear frames internos para los videos
    camera_frame1 = tk.Canvas(frame, width=300, height=300, bg="gray")
    camera_frame1.pack(side=tk.LEFT, padx=(0, 10))

    camera_frame2 = tk.Canvas(frame, width=300, height=300, bg="gray")
    camera_frame2.pack(side=tk.LEFT, padx=(10, 0))

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
    pass

if __name__ == '__main__':
    cameras = list_cameras()
    if not cameras:
        print("No se encontraron cámaras.")
    load_config()
    main(cameras)



   
