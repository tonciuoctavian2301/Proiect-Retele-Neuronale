import tkinter as tk
import cv2
import PIL.Image, PIL.ImageTk
import numpy as np
import os
import sys
from tensorflow.keras.models import load_model

# --- CĂI ---
CURRENT_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(os.path.dirname(CURRENT_SCRIPT_DIR))
MODEL_EYES_PATH = os.path.join(PROJECT_ROOT, "models", "optimized_model.h5")
MODEL_MOUTH_PATH = os.path.join(PROJECT_ROOT, "models", "model_mouth.h5")

sys.path.append(PROJECT_ROOT)


class DrowsinessApp:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)
        self.window.geometry("1200x800")

        # 1. ÎNCĂRCARE
        print(f"[INFO] Modele: {MODEL_EYES_PATH}")
        try:
            self.model_eyes = load_model(MODEL_EYES_PATH)
            self.model_mouth = load_model(MODEL_MOUTH_PATH)
            print("✅ Modele încărcate!")
        except Exception as e:
            print(f"❌ EROARE: {e}")

        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

        self.video_source = 0
        self.vid = MyVideoCapture(self.video_source)
        self.is_running = False

        # --- LOGICĂ ---
        self.score = 0
        self.IMG_SIZE = 64
        self.face_missing_counter = 0

        # --- GUI ---
        self.video_frame = tk.Frame(window, bg="black")
        self.video_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        self.canvas = tk.Canvas(self.video_frame, bg="black")
        self.canvas.pack(expand=True, fill=tk.BOTH)

        self.controls = tk.Frame(window, width=350, bg="#2c3e50")
        self.controls.pack(side=tk.RIGHT, fill=tk.Y)

        tk.Label(self.controls, text="SIA MONITOR", font=("Arial", 20, "bold"), bg="#2c3e50", fg="white").pack(pady=20)

        self.lbl_score = tk.Label(self.controls, text="Scor: 0", font=("Arial", 24, "bold"), bg="#2c3e50", fg="#f1c40f")
        self.lbl_score.pack(pady=10)

        self.lbl_mouth_val = tk.Label(self.controls, text="Valoare Gură: 0.00", font=("Arial", 14), bg="#2c3e50",
                                      fg="cyan")
        self.lbl_mouth_val.pack(pady=5)

        self.lbl_stare = tk.Label(self.controls, text="STARE: AȘTEPTARE", font=("Arial", 12, "bold"), bg="#2c3e50",
                                  fg="white")
        self.lbl_stare.pack(pady=10)

        self.btn_start = tk.Button(self.controls, text="PORNEȘTE CAMERA", font=("Arial", 12, "bold"), bg="#27ae60",
                                   fg="white", command=self.toggle_camera)
        self.btn_start.pack(pady=15, ipadx=10)

        tk.Button(self.controls, text="RESET SCOR", bg="#c0392b", fg="white", command=self.reset_score).pack(pady=5)

        # --- REGLAJE ---
        tk.Label(self.controls, text="__________________________", bg="#2c3e50", fg="gray").pack(pady=10)

        # Slider Sensibilitate OCHI
        tk.Label(self.controls, text="Sensibilitate OCHI:", bg="#2c3e50", fg="white").pack()
        self.slider_thresh = tk.Scale(self.controls, from_=0, to=100, orient=tk.HORIZONTAL, bg="#2c3e50", fg="white",
                                      length=250)
        self.slider_thresh.set(50)
        self.slider_thresh.pack(pady=5)

        self.inverse_logic = tk.BooleanVar(value=True)
        tk.Checkbutton(self.controls, text="Logic: Valoare Mică = OCHI ÎNCHIȘI", var=self.inverse_logic, bg="#2c3e50",
                       fg="orange", selectcolor="#2c3e50").pack(pady=5)

        self.use_fallback = tk.BooleanVar(value=True)
        tk.Checkbutton(self.controls, text="Lipsă Ochi = SOMN (Fallback)", var=self.use_fallback, bg="#2c3e50",
                       fg="lightgreen", selectcolor="#2c3e50").pack(pady=5)

        self.delay = 15
        self.update()

    def reset_score(self):
        self.score = 0
        self.lbl_score.config(text="Scor: 0")

    def toggle_camera(self):
        if not self.is_running:
            self.is_running = True
            self.btn_start.config(text="OPREȘTE", bg="#e67e22")
        else:
            self.is_running = False
            self.btn_start.config(text="PORNEȘTE", bg="#27ae60")

    def prepare_image(self, img_roi):
        try:
            gray = cv2.cvtColor(img_roi, cv2.COLOR_BGR2GRAY)
            resized = cv2.resize(gray, (self.IMG_SIZE, self.IMG_SIZE))
            normalized = resized / 255.0
            return np.reshape(normalized, (1, self.IMG_SIZE, self.IMG_SIZE, 1))
        except:
            return None

    def update(self):
        if self.is_running:
            ret, frame = self.vid.get_frame()
            if ret:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                # Face detection - Sensibilitate medie (neighbors=4)
                faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=4, minSize=(80, 80))

                eyes_closed_in_frame = False
                mouth_open_score = 0.0
                thresh = self.slider_thresh.get() / 100.0

                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (100, 100, 100), 1)

                    upper_face = frame[y:y + h // 2, x:x + w]
                    eyes = self.eye_cascade.detectMultiScale(upper_face, scaleFactor=1.1, minNeighbors=4)

                    # --- FALLBACK OCHI ---
                    if len(eyes) == 0 and self.use_fallback.get():
                        eyes_closed_in_frame = True
                        cv2.putText(frame, "LIPSA OCHI -> SOMN", (x, y - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                                    (0, 165, 255), 2)

                    for (ex, ey, ew, eh) in eyes:
                        input_data = self.prepare_image(upper_face[ey:ey + eh, ex:ex + ew])
                        if input_data is not None:
                            pred = self.model_eyes.predict(input_data, verbose=0)[0][0]

                            if self.inverse_logic.get():
                                is_closed = pred < thresh
                            else:
                                is_closed = pred > thresh

                            if is_closed:
                                eyes_closed_in_frame = True
                                color = (0, 0, 255)  # Rosu
                            else:
                                color = (0, 255, 0)  # Verde

                            cv2.rectangle(frame, (x + ex, y + ey), (x + ex + ew, y + ey + eh), color, 2)
                            cv2.putText(frame, f"{pred:.2f}", (x + ex, y + ey - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.4,
                                        color, 1)

                    # --- GURA (ZONA MĂRITĂ) ---
                    # Estimăm o zonă mai generoasă pentru gură
                    mx = x + int(w * 0.2)
                    my = y + int(h * 0.6)
                    mw = int(w * 0.6)
                    mh = int(h * 0.35)

                    # Desenăm zona gurii cu CYAN ca să vezi unde caută
                    cv2.rectangle(frame, (mx, my), (mx + mw, my + mh), (255, 255, 0), 1)

                    try:
                        mouth_roi = frame[my:my + mh, mx:mx + mw]
                        input_mouth = self.prepare_image(mouth_roi)
                        if input_mouth is not None:
                            pred_m = self.model_mouth.predict(input_mouth, verbose=0)[0][0]
                            mouth_open_score = pred_m

                            # Afișare scor gură lângă dreptunghi
                            cv2.putText(frame, f"{pred_m:.2f}", (mx, my + mh + 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                        (255, 255, 0), 1)

                            # PRAG GURĂ (Relaxat la 0.4)
                            if pred_m > 0.4:
                                cv2.putText(frame, "CASCAT!", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                                self.score += 2
                                # Facem chenarul gurii roșu când detectează
                                cv2.rectangle(frame, (mx, my), (mx + mw, my + mh), (0, 0, 255), 2)

                    except:
                        pass

                # --- UPDATE SCOR ---
                self.lbl_mouth_val.config(text=f"Valoare Gură: {mouth_open_score:.3f}")

                if eyes_closed_in_frame:
                    self.score += 1
                    self.lbl_stare.config(text="STARE: OCHI ÎNCHIȘI", fg="red")
                else:
                    self.score -= 3  # Scade moderat
                    self.lbl_stare.config(text="STARE: OCHI DESCHIȘI", fg="green")

                self.score = max(0, min(50, self.score))
                self.lbl_score.config(text=f"Scor: {self.score}")

                if self.score > 20:
                    cv2.putText(frame, "ALARMĂ!", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 4)
                    cv2.rectangle(frame, (0, 0), (frame.shape[1], frame.shape[0]), (0, 0, 255), 10)

                img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(img_rgb))
                self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

        self.window.after(self.delay, self.update)

    def close_app(self):
        self.window.destroy()
        self.vid.del_camera()


class MyVideoCapture:
    def __init__(self, video_source=0):
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened(): print("Nu pot deschide camera")

    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            return (ret, cv2.resize(frame, (640, 480))) if ret else (ret, None)
        return (False, None)

    def del_camera(self):
        if self.vid.isOpened(): self.vid.release()


if __name__ == "__main__":
    root = tk.Tk()
    app = DrowsinessApp(root, "Sistem Final - Mouth Fix")
    root.mainloop()