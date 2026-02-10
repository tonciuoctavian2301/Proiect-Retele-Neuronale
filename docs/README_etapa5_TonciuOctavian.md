# 📘 README – Etapa 5: Configurarea și Antrenarea Modelului RN

**Disciplina:** Rețele Neuronale  
**Instituție:** POLITEHNICA București – FIIR  
**Student:** Tonciu Octavian  
**Data predării:** 11.12.2025

---

## Scopul Etapei 5

Această etapă a constat în antrenarea efectivă a celor două modele de Rețele Neuronale Convoluționale (CNN) definite în etapa anterioară:
1.  **Model Ochi:** Pentru clasificarea stării Deschis/Închis.
2.  **Model Gură:** Pentru clasificarea stării Normal/Căscat.

Sistemul a fost antrenat pe un set de date hibrid (imagini publice + date originale generate cu camera proprie), respectând cerința de >40% date originale.



## 1. Configurare și Hiperparametri (Nivel 1 - Obligatoriu)

Am utilizat framework-ul **TensorFlow/Keras**. Mai jos este justificarea alegerii hiperparametrilor pentru procesul de antrenare.

| **Hiperparametru** | **Valoare Aleasă** | **Justificare** |
| :--- | :--- | :--- |
| **Learning Rate** | 0.001 (Adam) | Valoarea standard pentru optimizatorul Adam; oferă un echilibru optim între viteza de convergență și stabilitate, evitând blocarea în minime locale. |
| **Batch Size** | 32 | Compromis ideal pentru memoria GPU/CPU disponibilă. Un batch prea mic face antrenarea lentă și instabilă, unul prea mare poate duce la generalizare slabă. |
| **Număr Epoci** | 20 | Am setat o limită superioară de 20, combinată cu **Early Stopping**. Modelul converge rapid (în 5-10 epoci) datorită simplității imaginilor (64x64 grayscale). |
| **Optimizer** | Adam | Ales pentru capacitatea de a ajusta dinamic rata de învățare (Adaptive Learning Rate). Este standardul în industrie pentru CNN-uri simple. |
| **Loss Function** | Binary Crossentropy | Deoarece problema este una strict binară (Clasa 0 vs Clasa 1), aceasta este funcția matematică care penalizează cel mai corect erorile de clasificare. |
| **Activare Output** | Sigmoid | Obligatoriu pentru clasificare binară, deoarece returnează o probabilitate între 0 și 1. |

---

## 2. Metrici de Performanță pe Setul de Test

Datele au fost împărțite stratificat: **80% Antrenare** / **20% Testare**.
Rezultatele obținute pe datele de test (date noi, nevăzute de model):


**Dovezi generate:**
- Istoricul antrenării a fost salvat în: `results/training_history_OCHI.csv`
- Metricele detaliate sunt în: `results/test_metrics_OCHI.json`



## 3. Analiza Erorilor în Context Industrial (Nivel 2)

Deși acuratețea este mare, am analizat potențialele puncte slabe ale sistemului într-un scenariu real de condus.

### A. Pe ce clase ar putea greși modelul?
Din testele preliminare și analiza Matricei de Confuzie (`docs/charts/confusion_matrix_OCHI.png`), erorile tind să fie **False Positives** (Sistemul crede că ochiul e închis când e deschis).
*Cauza:* Clipitul rapid sau purtarea ochelarilor cu rame groase care acoperă pleoapa.

### B. Ce caracteristici ale datelor cauzează erori?
1.  **Lumina slabă:** Zgomotul din imagine ("purecii") poate fi interpretat greșit de filtrele convoluționale.
2.  **Reflexiile:** Reflexia ecranului în ochelari poate ascunde pupila, făcând ochiul să pară "alb" (închis).

### C. Ce implicații are asta pentru siguranță?
- **False Negative (Nedetectat):** Este eroarea CRITICĂ. Șoferul doarme, iar alarma nu sună.
- **False Positive (Alarmă Falsă):** Este doar deranjant.
*Decizie:* Am calibrat sistemul să fie ușor paranoic (sensibil). Preferăm o alarmă falsă decât un accident.

### D. Măsuri corective implementate în Aplicație (`detect_drowsiness.py`)
Pentru a combate erorile modelului, nu ne bazăm pe un singur cadru (frame). Am implementat un **algoritm de persistență (buffer)**:
> Alarma se declanșează DOAR dacă modelul prezice "Închis" timp de **15 cadre consecutive**. Astfel, erorile sporadice sau clipitul natural sunt ignorate.

## 4. Integrarea și Demonstrația Funcționării

Modelul antrenat (`models/model_eyes.h5`) a fost integrat cu succes în aplicația de monitorizare video.

**Screenshot Inferență Reală:**
Se poate observa în imaginea de mai jos cum sistemul detectează corect starea, calculează scorul și afișează alerta.


## Checklist Etapa 5

- [x] Model antrenat salvat în `models/model_eyes.h5` și `models/model_mouth.h5`.
- [x] Tabel cu Hiperparametri și justificări completat.
- [x] Grafice de Loss și Matricea de Confuzie generate în `docs/charts/`.
- [x] Aplicația UI (`detect_drowsiness.py`) folosește modelul antrenat, nu unul dummy.
- [x] Screenshot demonstrativ salvat în `docs/screenshots/inference_real.png`.