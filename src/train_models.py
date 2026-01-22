import os
import sys

# --- REPARATIE CĂI (Merge pe orice calculator) ---
# Aflăm unde este acest fișier (train_models.py)
CURRENT_FILE_PATH = os.path.abspath(__file__)
SRC_DIR = os.path.dirname(CURRENT_FILE_PATH)  # Folderul src
ROOT_DIR = os.path.dirname(SRC_DIR)  # Folderul proiectului (Detectia...)

# Construim căile folosind folderul rădăcină
DATA_PATH = os.path.join(ROOT_DIR, "data", "processed")
RESULTS_PATH = os.path.join(ROOT_DIR, "results")
CHARTS_PATH = os.path.join(ROOT_DIR, "docs", "charts")
MODELS_PATH = os.path.join(ROOT_DIR, "models")

print(f"DEBUG: Caut datele în: {DATA_PATH}")
# ------------------------------------------------

import numpy as np
import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, f1_score

# Asigurăm existența folderelor de ieșire
os.makedirs(RESULTS_PATH, exist_ok=True)
os.makedirs(CHARTS_PATH, exist_ok=True)
os.makedirs(MODELS_PATH, exist_ok=True)

IMG_SIZE = 64
EPOCHS = 20
BATCH_SIZE = 32


def build_cnn_model():
    model = Sequential([
        Conv2D(32, (3, 3), activation='relu', input_shape=(IMG_SIZE, IMG_SIZE, 1)),
        MaxPooling2D(2, 2),
        Conv2D(64, (3, 3), activation='relu'),
        MaxPooling2D(2, 2),
        Conv2D(128, (3, 3), activation='relu'),
        MaxPooling2D(2, 2),
        Flatten(),
        Dropout(0.5),
        Dense(64, activation='relu'),
        Dense(1, activation='sigmoid')
    ])
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return model


def train_specific_model(name, x_file, y_file, output_model_name):
    print(f"\n=== Începe antrenarea pentru: {name} ===")

    path_x = os.path.join(DATA_PATH, x_file)
    path_y = os.path.join(DATA_PATH, y_file)

    if not os.path.exists(path_x):
        print(f"EROARE CRITICĂ: Nu găsesc fișierul: {path_x}")
        print("Soluție: Dă click dreapta pe 'preprocessing.py' și alege RUN.")
        return

    # Încărcare
    X = np.load(path_x)
    y = np.load(path_y)
    print(f"   Am încărcat {len(X)} imagini.")

    # Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    # Antrenare
    model = build_cnn_model()
    early_stop = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)

    history = model.fit(
        X_train, y_train,
        epochs=EPOCHS,
        batch_size=BATCH_SIZE,
        validation_data=(X_test, y_test),
        callbacks=[early_stop]
    )

    # Salvare
    model.save(os.path.join(MODELS_PATH, output_model_name))
    pd.DataFrame(history.history).to_csv(os.path.join(RESULTS_PATH, f'training_history_{name}.csv'))

    print(f"✅ GATA! Modelul {name} a fost salvat.")


if __name__ == "__main__":
    train_specific_model("OCHI", "X_eyes.npy", "y_eyes.npy", "model_eyes.h5")
    train_specific_model("GURA", "X_mouth.npy", "y_mouth.npy", "model_mouth.h5")