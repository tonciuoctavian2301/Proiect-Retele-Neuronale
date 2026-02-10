import cv2
import os
import time



# Salvează imagini de la webcam în folderul data/raw

def collect_data(label_name="ochi_deschisi", num_samples=100):
    # Cale relativă către data/raw
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    save_path = os.path.join(base_dir, "data", "raw", label_name)

    if not os.path.exists(save_path):
        os.makedirs(save_path)

    cap = cv2.VideoCapture(0)
    count = 0

    print(f"--- Începem colectarea pentru: {label_name} ---")
    print("Apasă 's' pentru a salva o poză. Apasă 'q' pentru a ieși.")

    while count < num_samples:
        ret, frame = cap.read()
        if not ret: continue

        cv2.imshow("Data Collection", frame)
        key = cv2.waitKey(1)

        if key == ord('s'):
            img_name = os.path.join(save_path, f"{label_name}_{int(time.time())}_{count}.jpg")
            cv2.imwrite(img_name, frame)
            print(f"Salvat: {img_name}")
            count += 1
        elif key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    # Poți schimba eticheta aici când rulezi
    collect_data("test_capture", 10)