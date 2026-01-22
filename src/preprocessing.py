import os
import cv2
import numpy as np
import random

# --- CONFIGURĂRI ---
# Calea unde sunt folderele tale (asigură-te că numele sunt exacte!)
RAW_DIR = "../data/raw"
PROCESSED_DIR = "../data/processed"
IMG_SIZE = 64  # Toate imaginile vor fi redimensionate la 64x64 pixeli

# Aici definim perechile de foldere și etichetele lor
# 0 = Stare Normală (Sigur)
# 1 = Stare de Oboseală (Alertă)

# Configurare pentru OCHI
FOLDERS_EYES = [
    ("open_eyes", 0),  # Folderul cu ochi deschiși -> Eticheta 0
    ("closed_eyes", 1)  # Folderul cu ochi închiși -> Eticheta 1
]

# Configurare pentru GURĂ (Căscat)
FOLDERS_MOUTH = [
    ("nondrowsy", 0),  # Folderul normal (vorbind/gură închisă) -> Eticheta 0
    ("drowsy", 1)  # Folderul cu căscat -> Eticheta 1
]


def create_dataset(folders_list, save_name_x, save_name_y):
    """
    Citește imaginile din lista de foldere, le transformă și le salvează.
    """
    data = []
    print(f"\n--- Încep procesarea pentru setul: {save_name_x} ---")

    # Verificăm dacă există folderul de ieșire
    if not os.path.exists(PROCESSED_DIR):
        os.makedirs(PROCESSED_DIR)

    # Iterăm prin fiecare folder din listă
    for folder_name, label in folders_list:
        path = os.path.join(RAW_DIR, folder_name)

        # Verificare de siguranță
        if not os.path.exists(path):
            print(f"EROARE: Nu găsesc folderul '{folder_name}' în '{RAW_DIR}'!")
            print("Verifică dacă ai scris numele folderului corect (litere mari/mici, spații).")
            continue

        print(f"  > Încarc imagini din '{folder_name}' (Eticheta {label})...")

        count = 0
        files = os.listdir(path)

        for img_name in files:
            try:
                img_path = os.path.join(path, img_name)

                # 1. Citim imaginea și o facem Alb-Negru (Grayscale)
                # Slide 14: Flux video preferabil Infraroșu (deci monocrom)
                img_array = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

                if img_array is None:
                    continue  # Sărim peste fișierele care nu sunt imagini

                # 2. Redimensionare (Resize) la 64x64
                # Slide 8: Pre-procesare necesară pentru CNN
                resized_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))

                # 3. Adăugăm în listă
                data.append([resized_array, label])
                count += 1
            except Exception as e:
                pass  # Ignorăm erorile de citire

        print(f"    - Am procesat cu succes {count} imagini.")

    # 4. Amestecăm datele (Shuffle)
    # Important ca rețeaua să nu învețe ordinea (ex: întâi toate 'closed', apoi toate 'open')
    random.shuffle(data)

    # 5. Separăm Imaginile (X) de Etichete (y)
    x = []
    y = []

    for features, label in data:
        x.append(features)
        y.append(label)

    # 6. Conversie la NumPy Array și Normalizare
    # Reshape pentru a avea forma (Nr_Imagini, 64, 64, 1)
    x = np.array(x).reshape(-1, IMG_SIZE, IMG_SIZE, 1)

    # Normalizare: Împărțim la 255 ca valorile să fie între 0 și 1
    x = x / 255.0
    y = np.array(y)

    # 7. Salvarea fișierelor
    np.save(os.path.join(PROCESSED_DIR, f"{save_name_x}.npy"), x)
    np.save(os.path.join(PROCESSED_DIR, f"{save_name_y}.npy"), y)

    print(f"  > SALVAT! '{save_name_x}.npy' are dimensiunea {x.shape}")


def main():
    # Procesăm setul de date pentru OCHI
    create_dataset(FOLDERS_EYES, "X_eyes", "y_eyes")

    # Procesăm setul de date pentru GURĂ
    create_dataset(FOLDERS_MOUTH, "X_mouth", "y_mouth")

    print("\n=== Procesare Completă! ===")
    print(f"Fișierele au fost salvate în '{PROCESSED_DIR}'")


if __name__ == "__main__":
    main()