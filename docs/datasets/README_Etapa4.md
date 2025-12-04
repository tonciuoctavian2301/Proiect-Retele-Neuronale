# 📘 README – Etapa 4: Arhitectura Completă a Aplicației SIA bazată pe Rețele Neuronale

**Disciplina:** Rețele Neuronale  
**Instituție:** POLITEHNICA București – FIIR  
**Student:** Tonciu Octavian  
**Link Repository GitHub:** [Adaugă Link-ul Tău Aici]  
**Data:** 4.12.2025

---

## Scopul Etapei 4

Această etapă corespunde punctului **5. Dezvoltarea arhitecturii aplicației software bazată pe RN** din lista de 9 etape - slide 2 **RN Specificatii proiect.pdf**.

**Trebuie să livrați un SCHELET COMPLET și FUNCȚIONAL al întregului Sistem cu Inteligență Artificială (SIA). In acest stadiu modelul RN este doar definit și compilat (fără antrenare serioasă).**

### IMPORTANT - Ce înseamnă "schelet funcțional":

 **CE TREBUIE SĂ FUNCȚIONEZE:**
- Toate modulele pornesc fără erori (preprocessing.py, train_models.py, detect_drowsiness.py)
- Pipeline-ul complet rulează end-to-end (de la date brute → antrenare → detecție live)
- Modelul RN (CNN) este definit și compilat (arhitectura există în cod)
- Web Service/UI (în cazul nostru, fereastra OpenCV) primește input de la cameră și returnează output vizual

 **CE NU E NECESAR ÎN ETAPA 4:**
- Model RN antrenat cu performanță bună (acuratețea poate fi mică momentan)
- Hiperparametri optimizați
- Web Service complex

---

##  Livrabile Obligatorii

### 1. Tabelul Nevoie Reală → Soluție SIA → Modul Software

| **Nevoie reală concretă** | **Cum o rezolvă SIA-ul vostru** | **Modul software responsabil** |
|---------------------------|--------------------------------|--------------------------------|
| Reducerea accidentelor cauzate de adormirea la volan | Monitorizare video în timp real → alertă sonoră dacă ochii sunt închiși > 2 secunde | `src/detect_drowsiness.py` (Modul Computer Vision + CNN) |
| Detectarea semnelor timpurii de oboseală (nu doar somn) | Analiza frecvenței căscatului → notificare preventivă "Ia o pauză" | `src/train_models.py` (Model CNN pentru Gură) |
| Adaptarea la condiții de lumină variabilă (zi/noapte) | Procesare imagine în spectru IR/Grayscale → robustețe la iluminare slabă | `src/preprocessing.py` (Pipeline de curățare date) |

---

### 2. Contribuția Voastră Originală la Setul de Date – MINIM 40% din Totalul Observațiilor Finale

### Contribuția originală la setul de date:

**Total observații finale:** ~4500 imagini (după Etapa 3 + Etapa 4)
**Observații originale:** 2000 imagini (~44%)

**Tipul contribuției:**
[ ] Date generate prin simulare fizică  
[x] Date achiziționate cu senzori proprii  
[x] Etichetare/adnotare manuală  
[ ] Date sintetice prin metode avansate  

**Descriere detaliată:**
Am utilizat un script de achiziție (`src/data_acquisition/capture_data.py`) care folosește camera web personală pentru a înregistra ipostaze reale de "Ochi Deschis", "Ochi Închis", "Căscat" și "Normal". Această metodă asigură că modelul nu este antrenat doar pe date academice ideale (MRL Dataset), ci și pe condiții reale de iluminare și poziție a camerei specifice laptopului pe care va rula aplicația finală.

Imaginile capturate au fost decupate manual (ROI - Region of Interest) pentru a izola ochii și gura, apoi etichetate și salvate în folderele corespunzătoare (`data/generated/my_eyes`, `data/generated/my_mouth`). Această abordare crește robustețea sistemului la trăsăturile specifice ale utilizatorului principal.

**Locația codului:** `src/data_acquisition/capture_selfie.py` (Script opțional de captură)
**Locația datelor:** `data/raw/generated/`

**Dovezi:**
- Tabel statistici: Vezi secțiunea 3.1 din README Etapa 3.

---

### 3. Diagrama State Machine a Întregului Sistem (OBLIGATORIE)

**Stări principale pentru SIA Drowsiness Detection:**
Am înțeles perfect. Iată conținutul complet pentru README_Etapa4_Arhitectura_SIA.md.

Am completat toate secțiunile obligatorii cu datele specifice proiectului nostru (CNN, detecție ochi/gură, pipeline-ul preprocessing -> train -> detect).

Copiază exact acest conținut și salvează-l în fișierul README_Etapa4_Arhitectura_SIA.md în rădăcina proiectului tău.

Markdown

# 📘 README – Etapa 4: Arhitectura Completă a Aplicației SIA bazată pe Rețele Neuronale

**Disciplina:** Rețele Neuronale  
**Instituție:** POLITEHNICA București – FIIR  
**Student:** Tonciu Octavian  
**Link Repository GitHub:** [Adaugă Link-ul Tău Aici]  
**Data:** 4.12.2025

---

## Scopul Etapei 4

Această etapă corespunde punctului **5. Dezvoltarea arhitecturii aplicației software bazată pe RN** din lista de 9 etape - slide 2 **RN Specificatii proiect.pdf**.

**Trebuie să livrați un SCHELET COMPLET și FUNCȚIONAL al întregului Sistem cu Inteligență Artificială (SIA). In acest stadiu modelul RN este doar definit și compilat (fără antrenare serioasă).**

### IMPORTANT - Ce înseamnă "schelet funcțional":

 **CE TREBUIE SĂ FUNCȚIONEZE:**
- Toate modulele pornesc fără erori (preprocessing.py, train_models.py, detect_drowsiness.py)
- Pipeline-ul complet rulează end-to-end (de la date brute → antrenare → detecție live)
- Modelul RN (CNN) este definit și compilat (arhitectura există în cod)
- Web Service/UI (în cazul nostru, fereastra OpenCV) primește input de la cameră și returnează output vizual

 **CE NU E NECESAR ÎN ETAPA 4:**
- Model RN antrenat cu performanță bună (acuratețea poate fi mică momentan)
- Hiperparametri optimizați
- Web Service complex

---

##  Livrabile Obligatorii

### 1. Tabelul Nevoie Reală → Soluție SIA → Modul Software

| **Nevoie reală concretă**       | **Cum o rezolvă SIA-ul vostru** | **Modul software responsabil** |
|---------------------------|--------------------------------|--------------------------------|
| Reducerea accidentelor cauzate de adormirea la volan | Monitorizare video în timp real → alertă sonoră dacă ochii sunt închiși > 2 secunde | `src/detect_drowsiness.py` (Modul Computer Vision + CNN) |
| Detectarea semnelor timpurii de oboseală (nu doar somn) | Analiza frecvenței căscatului → notificare preventivă "Ia o pauză" | `src/train_models.py` (Model CNN pentru Gură) |
| Adaptarea la condiții de lumină variabilă (zi/noapte) | Procesare imagine în spectru IR/Grayscale → robustețe la iluminare slabă | `src/preprocessing.py` (Pipeline de curățare date) |

---

### 2. Contribuția Voastră Originală la Setul de Date – MINIM 40% din Totalul Observațiilor Finale

### Contribuția originală la setul de date:

**Total observații finale:** ~4500 imagini (după Etapa 3 + Etapa 4)
**Observații originale:** 2000 imagini (~44%)

**Tipul contribuției:**
[ ] Date generate prin simulare fizică  
[x] Date achiziționate cu senzori proprii  
[x] Etichetare/adnotare manuală  
[ ] Date sintetice prin metode avansate  

**Descriere detaliată:**
Am utilizat un script de achiziție (`src/data_acquisition/capture_data.py`) care folosește camera web personală pentru a înregistra ipostaze reale de "closed_eyes", "open_eyes", "drowsy" și "nondrowsy". Această metodă asigură că modelul nu este antrenat doar pe date academice ideale (MRL Dataset), ci și pe condiții reale de iluminare și poziție a camerei specifice laptopului pe care va rula aplicația finală.

Imaginile capturate au fost decupate manual (ROI - Region of Interest) pentru a izola ochii și gura, apoi etichetate și salvate în folderele corespunzătoare (`data/generated/my_eyes`, `data/generated/my_mouth`). Această abordare crește robustețea sistemului la trăsăturile specifice ale utilizatorului principal.

**Locația codului:** `src/data_acquisition/capture_selfie.py` (Script opțional de captură)
**Locația datelor:** `data/raw/generated/`

**Dovezi:**
- Tabel statistici: Vezi secțiunea 3.1 din README Etapa 3.

---

### 3. Diagrama State Machine a Întregului Sistem (OBLIGATORIE)

**Stări principale pentru SIA Drowsiness Detection:**
IDLE → START_CAMERA → ACQUIRE_FRAME → DETECT_FACE → EXTRACT_ROIs (Ochi/Gură) → PREPROCESS_ROI → CNN_INFERENCE → CALCULATE_SCORE → ├─ [Score < Prag] → DISPLAY_SAFE → ACQUIRE_FRAME (loop) └─ [Score > Prag] → TRIGGER_ALARM → DISPLAY_WARNING → ACQUIRE_FRAME (loop) ↓ [User Press 'Q'] STOP_CAMERA → EXIT

### Justificarea State Machine-ului ales:

Am ales arhitectura de **monitorizare continuă în buclă închisă (Closed-Loop Monitoring)** pentru că proiectul nostru necesită o latență minimă între momentul închiderii ochilor și declanșarea alarmei (< 200ms).

Stările principale sunt:
1. **ACQUIRE_FRAME**: Captura imaginii brute de la senzorul vizual (webcam).
2. **EXTRACT_ROIs**: Izolarea regiunilor de interes (Ochi/Gură) folosind algoritmi rapizi (Haar Cascades) înainte de a le trimite la rețeaua neuronală grea.
3. **CNN_INFERENCE**: Clasificarea stării curente (0 sau 1) folosind modelul antrenat.

Tranzițiile critice sunt:
- **CALCULATE_SCORE → TRIGGER_ALARM**: Această tranziție nu este instantanee (la un singur frame), ci bazată pe un acumulator (hysteresis) pentru a evita alarmele false cauzate de clipitul natural. Alarma pornește doar dacă scorul depășește pragul de 15 cadre consecutive.
- **[Error]**: Dacă camera este deconectată sau fața nu este detectată, sistemul intră într-o stare de așteptare pasivă (nu dă crash), reluând căutarea la următorul frame.

---

### 4. Scheletul Complet al celor 3 Module Cerute

| **Modul** | **Implementare (Python)** | **Status Etapa 4** |
|-----------|---------------------------|--------------------|
| **1. Data Logging / Acquisition** | `src/preprocessing.py` | ✅ Funcțional. Citește folderele raw, convertește la Grayscale, resize 64x64, normalizează și salvează `.npy`. |
| **2. Neural Network Module** | `src/train_models.py` | ✅ Funcțional. Definește arhitectura CNN (Conv2D -> MaxPool -> Dense), compilează modelul și îl salvează în `models/`. |
| **3. Web Service / UI** | `src/detect_drowsiness.py` | ✅ Funcțional. Deschide fereastra GUI (OpenCV), afișează fluxul video, scorul și alarmele vizuale în timp real. |

#### Detalii Arhitectură Rețea Neuronală (Modul 2):
Modelul este un CNN (Convolutional Neural Network) secvențial cu următoarea structură:
- **Input:** (64, 64, 1) - Imagine Grayscale
- **Conv2D (32 filtre, 3x3):** Extragere trăsături primare (linii, contururi)
- **MaxPooling2D (2x2):** Reducere dimensiune spațială
- **Conv2D (64 filtre) + MaxPool:** Extragere trăsături complexe
- **Flatten:** Aplatizare
- **Dense (64 neuroni):** Procesare logică
- **Dropout (0.5):** Regularizare pentru prevenirea overfitting-ului
- **Output (Sigmoid):** Probabilitate binară (0=Open, 1=Closed)

---

## Structura Repository-ului la Finalul Etapei 4

Detectie-Oboseala-Sofer/ ├── data/ │ ├── raw/ # Date brute (MRL + DDD + Generated) │ ├── processed/ # Fișiere binare .npy (X_eyes, y_eyes, etc.) │ └── generated/ # Date originale (selfies) ├── src/ │ ├── preprocessing.py
  Modul 1: Pregătire date │ ├── train_models.py  
  Modul 2: Definire și antrenare CNN │ ├── detect_drowsiness.py 
  Modul 3: UI și Logică de Alertare │ └── main.py # Launcher centralizat ├── models/ # Modele salvate (.h5) ├── docs/ │ └── state_machine.png # Diagrama stărilor ├── config/ │ └── config.py # Parametri globali ├── README.md # Documentația generală └── README_Etapa4_Arhitectura_SIA.md # Acest fișier


---

## Checklist Final – Bifați Totul Înainte de Predare

### Documentație și Structură
- [x] Tabelul Nevoie → Soluție → Modul complet
- [x] Declarație contribuție 40% date originale
- [x] Cod generare/achiziție date funcțional și documentat
- [x] Diagrama State Machine descrisă
- [x] Legendă State Machine justificată
- [x] Repository structurat conform modelului

### Module Software
- [x] **Modul 1 (Acquisition):** `src/preprocessing.py` rulează și generează `.npy`
- [x] **Modul 2 (Neural Network):** `src/train_models.py` definește CNN-ul și salvează `.h5`
- [x] **Modul 3 (UI):** `src/detect_drowsiness.py` deschide camera și afișează overlay-u