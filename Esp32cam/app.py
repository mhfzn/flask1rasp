import cv2
import urllib.request  # Untuk membuka dan membaca URL
import numpy as np
from src.utils import Park_classifier


def demostration():
    """Demonstrasi aplikasi sistem parkir menggunakan kamera ESP32."""
    
    # Parameter
    rect_width, rect_height = 225,126 # ukuran kotak nya harus di samakan dengan yang di utils.py
    carp_park_positions_path = "data/source/CarParkPos"
    url = 'http://192.168.190.73'  # URL lokal kamera ESP32

    # Membuat instance classifier yang menggunakan proses gambar dasar untuk klasifikasi
    classifier = Park_classifier(carp_park_positions_path, rect_width, rect_height)

    while True:
        try:
            # Membuka URL dan membaca gambar
            imgResponse = urllib.request.urlopen(url)
            imgNp = np.array(bytearray(imgResponse.read()), dtype=np.uint8)
            img = cv2.imdecode(imgNp, -1)  # Decode gambar

            if img is None:
                print("Error: Tidak dapat membaca gambar dari URL")
                continue

            # Rotasi gambar searah jarum jam
            img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)

            # Tidak perlu menggunakan cap.read() karena kita sudah memiliki img
            frame = img

            # Proses frame untuk klasifikasi
            prosessed_frame = classifier.implement_process(frame)

            # Menggambar status tempat parkir pada gambar
            denoted_image = classifier.classify(image=frame, prosessed_image=prosessed_frame)

            # Menampilkan hasil
            cv2.imshow("Car Park Image", denoted_image)

            # Kondisi keluar
            k = cv2.waitKey(1)
            if k & 0xFF == ord('q'):
                break

            if k & 0xFF == ord('s'):
                cv2.imwrite("output.jpg", denoted_image)

        except Exception as e:
            print(f"Error: {e}")


    # Mengembalikan sumber daya
    cv2.destroyAllWindows()

if __name__ == "__main__":
    demostration()
