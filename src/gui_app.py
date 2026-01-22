import tkinter as tk
import cv2
import PIL.Image, PIL.ImageTk
import numpy as np
import os
import sys
from tensorflow.keras.models import load_model

# --- COD ACTUALIZAT PENTRU ETAPA 6 ---
CURRENT_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_SCRIPT_DIR)

# AICI E MODIFICAREA: Încărcăm modelul OPTIMIZAT pentru ochi
MODEL_EYES_PATH = os.path.join(PROJECT_ROOT, "models", "optimized_model.h5")
# Modelul pentru gură poate rămâne cel vechi dacă nu l-ai optimizat separat
MODEL_MOUTH_PATH = os.path.join(PROJECT_ROOT, "models", "model_mouth.h5")


class DrowsinessApp:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)
        self.window.geometry("1100x700")

        # 1. ÎNCĂRCAREA MODELELOR
        print("[INFO] Se încarcă modelele...")
        try:
            self.model_eyes = load_model(MODEL_EYES_PATH)
            self.model_mouth = load_model(MODEL_MOUTH_PATH)
            print("✅ Modele încărcate! Gata de treabă.")
        except Exception as e:
            print(f"❌ EROARE: Nu găsesc modelele! {e}")
            sys.exit()

        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

        self.video_source = 0
        self.vid = MyVideoCapture(self.video_source)
        self.is_running = False

        # --- CONFIGURĂRI AUTOMATE ---
        self.score = 0
        self.IMG_SIZE = 64

        # Setări sensibilitate (Nu le mai modifici manual)
        self.ALARM_TRIGGER = 30  # La cât scor sună alarma
        self.EYE_THRESHOLD = 0.5  # Punctul de trecere (Standard)

        # --- INTERFAȚA GRAFICĂ ---
        # Stânga: Video
        self.video_frame = tk.Frame(window, bg="black")
        self.video_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        self.canvas = tk.Canvas(self.video_frame, bg="black")
        self.canvas.pack(expand=True, fill=tk.BOTH)

        # Dreapta: Panou Control
        self.controls = tk.Frame(window, width=350, bg="#222f3e")
        self.controls.pack(side=tk.RIGHT, fill=tk.Y)

        # Elemente Vizuale
        tk.Label(self.controls, text="SIA - MONITORIZARE", font=("Arial", 20, "bold"), bg="#222f3e", fg="white").pack(
            pady=30)

        # STATUS (Sigur / Pericol)
        self.lbl_status = tk.Label(self.controls, text="STANDBY", font=("Arial", 24, "bold"), bg="gray", fg="white",
                                   width=15)
        self.lbl_status.pack(pady=20)

        # SCOR (Cifra mare)
        self.lbl_score = tk.Label(self.controls, text="Scor: 0", font=("Arial", 22, "bold"), bg="#222f3e", fg="#feca57")
        self.lbl_score.pack(pady=10)

        # Buton Pornire
        self.btn_start = tk.Button(self.controls, text="PORNEȘTE CAMERA", font=("Arial", 14, "bold"), bg="#10ac84",
                                   fg="white", command=self.toggle_camera)
        self.btn_start.pack(pady=20, ipadx=10, ipady=5)

        # Buton Resetare Urgență
        tk.Button(self.controls, text="RESET SCOR", font=("Arial", 10), bg="#ff6b6b", fg="white",
                  command=self.reset_score).pack(pady=10)

        # --- REGLAJ UNIC (IMPORTANT) ---
        tk.Label(self.controls, text="__________________________", bg="#222f3e", fg="gray").pack(pady=20)
        tk.Label(self.controls, text="Dacă scorul crește invers:", bg="#222f3e", fg="white").pack()

        # Checkbox simplu
        self.inverse_logic = tk.BooleanVar(value=True)
        tk.Checkbutton(self.controls, text="Inversează Logica", var=self.inverse_logic, bg="#222f3e", fg="orange",
                       selectcolor="#222f3e", font=("Arial", 11)).pack(pady=10)

        self.delay = 15
        self.update()

    def reset_score(self):
        self.score = 0
        self.lbl_score.config(text="Scor: 0")

    def toggle_camera(self):
        if not self.is_running:
            self.is_running = True
            self.btn_start.config(text="OPREȘTE CAMERA", bg="#ee5253")
            self.lbl_status.config(text="ACTIV", bg="green")
        else:
            self.is_running = False
            self.btn_start.config(text="PORNEȘTE CAMERA", bg="#10ac84")
            self.lbl_status.config(text="STANDBY", bg="gray")

    def prepare_image(self, img_roi):
        try:
            gray = cv2.cvtColor(img_roi, cv2.COLOR_BGR2GRAY)
            resized = cv2.resize(gray, (self.IMG_SIZE, self.IMG_SIZE))
            normalized = resized / 255.0
            reshaped = np.reshape(normalized, (1, self.IMG_SIZE, self.IMG_SIZE, 1))
            return reshaped
        except:
            return None

    def update(self):
        if self.is_running:
            ret, frame = self.vid.get_frame()
            if ret:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                # Detectăm fețele
                faces = self.face_cascade.detectMultiScale(gray, 1.1, 5, minSize=(100, 100))

                eyes_closed_now = False

                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (100, 100, 100), 1)

                    # --- ANALIZĂ OCHI ---
                    upper_face = frame[y:y + h // 2, x:x + w]
                    eyes = self.eye_cascade.detectMultiScale(upper_face, 1.1, 5)

                    for (ex, ey, ew, eh) in eyes:
                        input_data = self.prepare_image(upper_face[ey:ey + eh, ex:ex + ew])

                        if input_data is not None:
                            # 1. Obținem predicția (ex: 0.1 sau 0.9)
                            pred = self.model_eyes.predict(input_data, verbose=0)[0][0]

                            # 2. DECIDEM AUTOMAT DACA E INCHIS
                            # Verificăm bifa de "Inverse Logic"
                            if self.inverse_logic.get():
                                is_closed = pred < self.EYE_THRESHOLD
                            else:
                                is_closed = pred > self.EYE_THRESHOLD

                            # 3. VIZUALIZARE (Verde = Deschis, Roșu = Închis)
                            color = (0, 0, 255) if is_closed else (0, 255, 0)
                            cv2.rectangle(frame, (x + ex, y + ey), (x + ex + ew, y + ey + eh), color, 2)

                            # Scriem valoarea ca să vezi ce zice AI-ul
                            cv2.putText(frame, f"{pred:.2f}", (x + ex, y + ey - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                        color, 1)

                            if is_closed:
                                eyes_closed_now = True

                    # --- ANALIZĂ GURĂ (Bonus) ---
                    try:
                        mx, my, mw, mh = x + int(w * 0.2), y + int(h * 0.6), int(w * 0.6), int(h * 0.4)
                        input_mouth = self.prepare_image(frame[my:my + mh, mx:mx + mw])
                        if input_mouth is not None:
                            pred_mouth = self.model_mouth.predict(input_mouth, verbose=0)[0][0]
                            if pred_mouth > 0.6:
                                cv2.putText(frame, "CASCAT", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                                self.score += 1  # Creștere ușoară la căscat
                                cv2.rectangle(frame, (mx, my), (mx + mw, my + mh), (0, 0, 255), 2)
                    except:
                        pass

                # --- CALCUL AUTOMAT SCOR ---
                if eyes_closed_now:
                    self.score += 1  # Crește dacă sunt închiși
                else:
                    self.score -= 4  # Scade RAPID dacă sunt deschiși (revenire automată)

                # Ținem scorul între 0 și 100
                self.score = max(0, min(100, self.score))
                self.lbl_score.config(text=f"Scor: {self.score}")

                # --- ALARMA ---
                if self.score >= self.ALARM_TRIGGER:
                    self.lbl_status.config(text="TREZEȘTE-TE!", bg="red")
                    cv2.rectangle(frame, (0, 0), (frame.shape[1], frame.shape[0]), (0, 0, 255), 15)
                elif self.score > 10:
                    self.lbl_status.config(text="ATENȚIE", bg="orange")
                else:
                    self.lbl_status.config(text="SIGUR", bg="green")

                # Afișare imagine
                img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(img_rgb))
                self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

        self.window.after(self.delay, self.update)

    def close_app(self):
        self.window.destroy()
        self.vid.del_camera()


# Clasa pentru cameră (Optimizată)
class MyVideoCapture:
    def __init__(self, video_source=0):
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError("Nu pot deschide camera video")

    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                return (ret, cv2.resize(frame, (640, 480)))
            else:
                return (ret, None)
        return (False, None)

    def del_camera(self):
        if self.vid.isOpened():
            self.vid.release()


if __name__ == "__main__":
    root = tk.Tk()
    app = DrowsinessApp(root, "Sistem Monitorizare")
    root.mainloop()