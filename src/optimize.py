import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout, Input
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score, f1_score

# --- CĂI AUTOMATE ---
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(CURRENT_DIR)
DATA_PATH = os.path.join(ROOT_DIR, "data", "processed")
RESULTS_PATH = os.path.join(ROOT_DIR, "results")
MODELS_PATH = os.path.join(ROOT_DIR, "models")
DOCS_PATH = os.path.join(ROOT_DIR, "docs")

os.makedirs(RESULTS_PATH, exist_ok=True)
os.makedirs(MODELS_PATH, exist_ok=True)
os.makedirs(DOCS_PATH, exist_ok=True)

# Încărcare date OCHI (Focusul principal)
print("[INFO] Se încarcă datele pentru optimizare...")
try:
    X = np.load(os.path.join(DATA_PATH, "X_eyes.npy"))
    y = np.load(os.path.join(DATA_PATH, "y_eyes.npy"))
except:
    print("EROARE: Nu găsesc X_eyes.npy! Rulează preprocessing.py întâi.")
    exit()

# Split date
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)


def build_model(filters, dropout, lr):
    model = Sequential([
        Input(shape=(64, 64, 1)),
        Conv2D(filters, (3, 3), activation='relu'),
        MaxPooling2D(2, 2),
        Conv2D(filters * 2, (3, 3), activation='relu'),
        MaxPooling2D(2, 2),
        Flatten(),
        Dropout(dropout),
        Dense(64, activation='relu'),
        Dense(1, activation='sigmoid')
    ])
    model.compile(optimizer=Adam(learning_rate=lr), loss='binary_crossentropy', metrics=['accuracy'])
    return model


# --- DEFINIREA CELOR 4 EXPERIMENTE (Cerință Etapa 6) ---
experiments = [
    {"name": "Exp1_Baseline", "filters": 32, "dropout": 0.5, "lr": 0.001, "batch": 32},
    {"name": "Exp2_HighLR", "filters": 32, "dropout": 0.5, "lr": 0.01, "batch": 32},
    {"name": "Exp3_BigBatch", "filters": 32, "dropout": 0.5, "lr": 0.001, "batch": 64},
    {"name": "Exp4_Optimized", "filters": 64, "dropout": 0.3, "lr": 0.0005, "batch": 32}  # Model mai complex
]

results_list = []
best_acc = 0
best_model_name = ""

print(f"\n[INFO] Începe rularea a {len(experiments)} experimente...")

for exp in experiments:
    print(f"\n--- Rulare {exp['name']} ---")
    model = build_model(exp['filters'], exp['dropout'], exp['lr'])

    early_stop = EarlyStopping(monitor='val_loss', patience=3, restore_best_weights=True)

    # Antrenare
    history = model.fit(
        X_train, y_train,
        epochs=15,  # Număr mic pentru testare rapidă, poți pune 50
        batch_size=exp['batch'],
        validation_data=(X_test, y_test),
        callbacks=[early_stop],
        verbose=0  # Să nu umple consola
    )

    # Evaluare
    y_pred = (model.predict(X_test) > 0.5).astype("int32")
    acc = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred, average='macro')

    print(f"   REZULTAT: Accuracy={acc:.4f}, F1={f1:.4f}")

    # Salvare în listă pentru CSV
    results_list.append({
        "Experiment": exp['name'],
        "Accuracy": acc,
        "F1_Score": f1,
        "Filters": exp['filters'],
        "LR": exp['lr'],
        "Dropout": exp['dropout']
    })

    # Salvare cel mai bun model
    if acc > best_acc:
        best_acc = acc
        best_model_name = exp['name']
        model.save(os.path.join(MODELS_PATH, "optimized_model.h5"))

        # Generare Confusion Matrix pentru cel mai bun model (Cerință Etapa 6)
        cm = confusion_matrix(y_test, y_pred)
        plt.figure(figsize=(6, 5))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
        plt.title(f'Confusion Matrix - {exp["name"]}')
        plt.savefig(os.path.join(DOCS_PATH, "confusion_matrix_optimized.png"))
        plt.close()

        # Salvare metrici finale JSON
        final_metrics = {
            "model": "optimized_model.h5",
            "test_accuracy": acc,
            "test_f1_macro": f1,
            "best_experiment": exp['name']
        }
        with open(os.path.join(RESULTS_PATH, "final_metrics.json"), "w") as f:
            json.dump(final_metrics, f, indent=4)

# Salvare Tabel Comparativ CSV (Cerință Etapa 6)
df_results = pd.DataFrame(results_list)
df_results.to_csv(os.path.join(RESULTS_PATH, "optimization_experiments.csv"), index=False)

print(f"\n[SUCCES] Optimizare completă!")
print(f"Cel mai bun model: {best_model_name} (Acc: {best_acc:.4f})")
print(f"Model salvat în: models/optimized_model.h5")
print(f"Tabel rezultate: results/optimization_experiments.csv")