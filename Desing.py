
# Importamos las librerías necesarias
from pathlib import Path
from PIL import Image as Pil_image, ImageTk as Pil_imageTk
from tkinter import Button, Label, PhotoImage, ttk, messagebox
from datetime import datetime
import tkinter as tk
import cv2
import os
import ctypes
from screeninfo import get_monitors

global cameras_list

# Definimos las cámaras a utilizar
camerasLevel = [[0, 1], [2, 3], [4, 5]]
config_path = Path('config.txt')

nivel_actual = 0
def inicio():
    def cambio():
        root.destroy()
        main() 
    root = tk.Tk()
    root.overrideredirect(True)
    
    imagen_fondo = tk.PhotoImage(file="xd.png")

    # Establecer la imagen de fondo en la ventana
    background_label = tk.Label(root, image=imagen_fondo)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
    root.minsize(1000, 600)
    background_label.config(bg='white')
    wtotal = root.winfo_screenwidth()
    htotal = root.winfo_screenheight()
    wventana = 1000
    hventana = 600
    pwidth = round(wtotal/2-wventana/2)
    pheight = round(htotal/2-hventana/2)
    root.geometry(str(wventana)+"x"+str(hventana)+"+"+str(pwidth)+"+"+str(pheight))
    
   



   
    imagen_continuar = tk.PhotoImage(file="Continue.png")
    imagen_continuar = imagen_continuar.subsample(13)  # 13Submuestrea la imagen por un factor de 15

    # Botón "Continuar" con imagen redimensionada
    button_continue = tk.Button(root, image=imagen_continuar, command=cambio, bg="white", bd=0)
    button_continue.pack(side=tk.RIGHT, anchor='se', padx=20, pady=20)

    


    imagen_cerrar = tk.PhotoImage(file="Close.png")
    imagen_cerrar = imagen_cerrar.subsample(17) #17

    # Botón "Cerrar" con imagen
    button_close = tk.Button(root, image=imagen_cerrar, command=root.destroy, bg="white", bd=0)
    button_close.pack(side=tk.LEFT, anchor='ne',padx=20, pady=20)
    
   
    
    
    root.mainloop()

  
def open_config():
    def save_config():
        # Logic to save the selected camera configuration
        print("Configuration Guardada")
        for i in range(3):
            if(combos_camera_config[i*2].current()==combos_camera_config[i*2+1].current()):
                print("Error: Las cámaras no pueden ser iguales")
                messagebox.showerror(message="Las cámaras de un mismo piso deben ser distintas", title="Error en la selección de cámaras")
                return
        with open(config_path, 'w') as file:
            for i in range(3):
                for j in range(2):
                    camerasLevel[i][j] = combos_camera_config[i*2+j].current()
                    file.write(f"{camerasLevel[i][j]} ")
                file.write("\n")
        config_window.destroy()
        update_cameras(nivel_actual, '', tk.Label())

    config_window = tk.Toplevel(root)
    config_window.title("Configuracion")
    config_window.overrideredirect(True)
    
    
    config_window.grab_set()
    combos_camera_config = []

    ###########################################
    #  Obtenemos el largo y  ancho de la pantalla
    wtotal = config_window.winfo_screenwidth()
    htotal = config_window.winfo_screenheight()
    #  Guardamos el largo y alto de la ventana
    wventana = 370
    hventana = 200

    #  Aplicamos la siguiente formula para calcular donde debería posicionarse
    pwidth = round(wtotal/2-wventana/2)
    pheight = round(htotal/2-hventana/2)

    #  Se lo aplicamos a la geometría de la ventana
    config_window.geometry(str(wventana)+"x"+str(hventana)+"+"+str(pwidth)+"+"+str(pheight))
    ############################
    
    label = tk.Label(config_window, text="Configuracion ", font=("Arial", 15),fg="#2E6EA6",bg="#F2F2F2")
    label.pack( pady=0)

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

    # Add a button for saving the configurationxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    cancelar_button = tk.Button(config_window, text="Cancelar", command=config_window.destroy,bg="#2E6EA6", fg="black", font=("Arial", 10))
    cancelar_button.pack(side=tk.LEFT, padx=100, pady=0)
    save_button = tk.Button(config_window, text="Guardar", command=save_config,bg="#2E6EA6", fg="black", font=("Arial", 10))
    save_button.pack(side=tk.LEFT, padx=0, pady=0)
    

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

def report():
    print("Presionaste el boton de reportes")
    videoCams = [camera1, camera2]
    folderName = datetime.now().strftime("%d-%m-%Y %H.%M")
    folderPath = Path(f"{folderName} Nivel {nivel_actual+1}")
    if not os.path.exists(folderPath):
        os.makedirs(folderPath)
    for i in range(2):
        take_pic(videoCams[i], f"{folderPath}/screenShotCamera{i}.png")

def take_pic(camera, path):
    ret, frame = camera.read()
    rgb_frame = frame[:, :, ::-1]
    img = Pil_image.fromarray(rgb_frame)
    img.save(path)
    print("Photo captured successfully.")



def main():
    global root, camera1, camera2, camera_frame1, camera_frame2

    
    root = tk.Tk()
    #root.overrideredirect(True)
    #root.resizable(False,False)
    root.minsize(1000, 600)
    bg_photo=PhotoImage(file='xd.png')
   
    root.geometry('1000x600')
    root.title("Webcam viewer")
    icono_chico = tk.PhotoImage(file="16.png")
    icono_grande = tk.PhotoImage(file="32.png")
    root.iconphoto(False, icono_grande, icono_chico)

    root.iconphoto(True, icono_chico)
    wtotal = root.winfo_screenwidth()
    htotal = root.winfo_screenheight()
    wventana = 1000
    hventana = 600
    pwidth = round(wtotal/2-wventana/2)
    pheight = round(htotal/2-hventana/2)
    root.geometry(str(wventana)+"x"+str(hventana)+"+"+str(pwidth)+"+"+str(pheight))
    icono = tk.PhotoImage(file="icono.png")
    root.config(bg='white')
    #root.iconphoto(True,icono)

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
    frame.configure(background="#FFFFFF")
    frame.pack(padx=20, pady=20)

    # Agregar un label al frame
    label = tk.Label(frame, text="Nivel "+ str(nivel_actual+1), font=("Arial", 24),fg="#2E6EA6",bg="#FFFFFF")
    label.pack( pady=0)

    # Definir acciones para cada botón
    button_actions = [lambda index=i, text=f"Nivel {i+1}": update_cameras(index, text, label) for i in range(3)]

    # Agregar botones al frame
    buttons_frame = tk.Frame(root)
    buttons_frame.configure(background="#ffffff")
    buttons_frame.pack(side=tk.TOP, pady=0)

    button_reports = tk.Button(buttons_frame, text="Módulo de Reportes", command=report, bg="#2E6EA6", fg="black", font=("Arial", 14))
    button_reports.pack(side=tk.LEFT, padx=20)

    button_reports2 = tk.Label(buttons_frame ,text="         ",bg="#ffffff", font=("Helvetica", 24))
    button_reports2.pack(side=tk.LEFT, padx=0)

    for i, action in enumerate(button_actions):
        button = tk.Button(buttons_frame, text=f"Nivel {i+1}", command=action, bg="#2E6EA6", fg="black", font=("Arial", 14))
        button.pack(side=tk.LEFT, padx=20)

    # Crear botones adicionales



    button_config = tk.Button(buttons_frame, text="Configuración", command=open_config, bg="#2E6EA6", fg="black", font=("Helvetica", 14))
    button_config.pack(side=tk.RIGHT, padx=20)
    button_reports2 = tk.Label(buttons_frame ,text="          ",bg="#ffffff", font=("Helvetica", 24))
    button_reports2.pack(side=tk.RIGHT, padx=20)

    # Crear frames internos para los videos
    camera_frame1 = tk.Canvas(frame, width=300, height=300, bg="white")
    camera_frame1.pack(side=tk.LEFT, padx=(0, 10), pady=13)

    camera_frame2 = tk.Canvas(frame, width=300, height=300, bg="white")
    camera_frame2.pack(side=tk.LEFT, padx=(10, 0), pady=13)

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
            if int(level_config[0]) == int(level_config[1]):
                messagebox.showwarning(message="Hubo un error en la carga de la configuración", title="Error cargando ")
                return
            camerasLevel[i] = [int(level_config[0]), int(level_config[1])]


cameras_list = list_cameras()
if not cameras_list:
    print("No se encontraron cámaras.")
load_config()
inicio()




   
