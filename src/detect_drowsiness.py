import cv2
import numpy as np
import os
import sys
from tensorflow.keras.models import load_model

# --- 1. CONFIGURARE ---
# Daca ochii stau tot timpul VERZI cand ii inchizi, schimba asta in True
# Daca stau tot timpul ROSII cand ii deschizi, schimba in False
INVERSEAZA_OCHI = True

CURRENT_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_SCRIPT_DIR)
MODEL_EYES_PATH = os.path.join(PROJECT_ROOT, "models", "model_eyes.h5")
MODEL_MOUTH_PATH = os.path.join(PROJECT_ROOT, "models", "model_mouth.h5")

IMG_SIZE = 64
ALARM_THRESHOLD = 40

# --- 2. INCARCARE MODELE ---
print("Se incarca modelele...")
try:
    model_eyes = load_model(MODEL_EYES_PATH)
    model_mouth = load_model(MODEL_MOUTH_PATH)
    print("✅ Modele incarcate!")
except Exception as e:
    print(f"EROARE: Nu pot incarca modelele. {e}")
    sys.exit()

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')


def prepare_image(img_roi):
    try:
        gray = cv2.cvtColor(img_roi, cv2.COLOR_BGR2GRAY)
        resized = cv2.resize(gray, (IMG_SIZE, IMG_SIZE))
        normalized = resized / 255.0
        reshaped = np.reshape(normalized, (1, IMG_SIZE, IMG_SIZE, 1))
        return reshaped
    except:
        return None


def main():
    cap = cv2.VideoCapture(0)
    score = 0

    print("--- DEBUGGING ---")
    print(f"Logica Ochi Inversata: {INVERSEAZA_OCHI}")
    print("Uita-te la numarul de deasupra ochiului!")
    print("-----------------")

    while True:
        ret, frame = cap.read()
        if not ret: break

        height, width = frame.shape[:2]
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detectie fata
        faces = face_cascade.detectMultiScale(gray, 1.1, 5, minSize=(100, 100))
        cv2.rectangle(frame, (0, height - 60), (width, height), (0, 0, 0), -1)

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 1)

            # --- OCHI ---
            upper_face = frame[y:y + h // 2, x:x + w]
            eyes = eye_cascade.detectMultiScale(upper_face, 1.1, 5)

            for (ex, ey, ew, eh) in eyes:
                eye_roi = upper_face[ey:ey + eh, ex:ex + ew]
                input_data = prepare_image(eye_roi)

                if input_data is not None:
                    pred = model_eyes.predict(input_data, verbose=0)[0][0]

                    # LOGICA FLEXIBILA
                    # Unii antreneaza 0=Inchis, altii 1=Inchis. Aici facem switch-ul.
                    if INVERSEAZA_OCHI:
                        is_closed = pred < 0.5  # Daca e mic (0.1) inseamna INCHIS
                    else:
                        is_closed = pred > 0.5  # Daca e mare (0.9) inseamna INCHIS

                    # Afisam numarul ca sa intelegem ce se intampla
                    val_text = f"{pred:.2f}"

                    if is_closed:
                        score += 1
                        cv2.rectangle(frame, (x + ex, y + ey), (x + ex + ew, y + ey + eh), (0, 0, 255), 2)
                        cv2.putText(frame, val_text, (x + ex, y + ey - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255),
                                    1)
                    else:
                        score -= 2
                        cv2.rectangle(frame, (x + ex, y + ey), (x + ex + ew, y + ey + eh), (0, 255, 0), 2)
                        cv2.putText(frame, val_text, (x + ex, y + ey - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0),
                                    1)

            # --- GURA ---
            mx, my, mw, mh = x + int(w * 0.2), y + int(h * 0.6), int(w * 0.6), int(h * 0.4)
            cv2.rectangle(frame, (mx, my), (mx + mw, my + mh), (100, 100, 100), 1)

            try:
                mouth_roi = frame[my:my + mh, mx:mx + mw]
                input_mouth = prepare_image(mouth_roi)
                if input_mouth is not None:
                    pred_mouth = model_mouth.predict(input_mouth, verbose=0)[0][0]
                    if pred_mouth > 0.5:
                        cv2.putText(frame, "CASCAT!", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                        cv2.rectangle(frame, (mx, my), (mx + mw, my + mh), (0, 0, 255), 2)
                        score += 2
            except:
                pass

        score = max(0, min(50, score))
        if score > ALARM_THRESHOLD:
            cv2.putText(frame, "TREZESTE-TE!", (width // 2 - 150, height // 2), cv2.FONT_HERSHEY_SIMPLEX, 2,
                        (0, 0, 255), 4)
            cv2.rectangle(frame, (0, 0), (width, height), (0, 0, 255), 10)

        cv2.putText(frame, f"Scor: {score}", (10, height - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv2.imshow('SIA Demo', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'): break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()