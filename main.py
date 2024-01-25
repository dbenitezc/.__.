import cv2
#crear diseno de botones

# interfaz completa
def list_cameras():
    cameras = []
    for i in range(cv2.CAP_DSHOW, cv2.CAP_DSHOW + 10):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            cameras.append(i)
            cap.release()
    return cameras

def main(camera_index):
    cap = cv2.VideoCapture(camera_index)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        cv2.imshow('Webcam Input', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    cameras = list_cameras()
    if not cameras:
        print("No cameras found.")
    else:
        print("Available cameras:")
        for i, cam in enumerate(cameras):
            print(f"{i}: Camera {cam}")

        camera_index = int(input("Enter the camera index to use: "))
        if 0 <= camera_index < len(cameras):
            main(cameras[camera_index])
        else:
            print("Invalid camera index.")