# Phishing Detection

Projekat za detekciju phishing email poruka koji se sastoji iz 3 glavna dela:

- ML pipeline (preprocesiranje + treniranje modela)
- FastAPI servis za predikciju
- Firefox ekstenzija za analizu poruka direktno u Gmail-u

## Sta je u projektu

Struktura:

```text
phishingDetection/
├── data/
│   ├── phishing_emails.csv
│   └── preprocessed_data.pkl (generise se)
├── extension/
│   ├── manifest.json
│   ├── background.js
│   ├── content.js
│   ├── popup.html
│   ├── popup.css
│   └── popup.js
├── models/
│   └── phishing_detector.pkl (generise se)
├── outputs/
│   └── training_YYYYMMDD_HHMMSS.log (generise se)
├── src/
│   ├── preprocessData.py
│   ├── logreg.py
│   ├── trainModel.py
│   ├── predictPhishing.py
│   └── api_server.py
├── requirements.txt
└── README.md
```

Opis glavnih fajlova:

- `src/preprocessData.py`: cita `data/phishing_emails.csv`, pravi TF-IDF reprezentaciju teksta i cuva rezultat u `data/preprocessed_data.pkl`
- `src/logreg.py`: custom implementacija logisticke regresije (gradient descent + L2 regularizacija)
- `src/trainModel.py`: trenira model nad preprocesiranim podacima, stampa classification report, cuva model u `models/phishing_detector.pkl` i log u `outputs/`
- `src/predictPhishing.py`: lokalni test predikcije iz skripte
- `src/api_server.py`: FastAPI server sa endpoint-ima `GET /health` i `POST /predict`
- `extension/*`: Firefox ekstenzija koja cita otvoreni Gmail email i salje tekst ka lokalnom API-ju

## Zahtevi

- Python 3.10+
- Firefox (za browser ekstenziju)

## Instalacija i priprema okruzenja

U root direktorijumu projekta pokreni:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Tok pokretanja (od nule)

Ako pokreces projekat prvi put, prati redosled ispod.

### 1) Preprocesiranje podataka

```bash
python3 src/preprocessData.py
```

Ova komanda:

- ucitava `data/phishing_emails.csv`
- primenjuje `TfidfVectorizer(max_features=5000, ngram_range=(1, 2))`
- cuva `(X, y, vectorizer)` u `data/preprocessed_data.pkl`

### 2) Treniranje modela

```bash
python3 src/trainModel.py
```

Ova komanda:

- ucitava `data/preprocessed_data.pkl`
- deli skup na train/test (`test_size=0.2`)
- trenira `LogisticRegression` iz `src/logreg.py`
- stampa classification report u terminal
- cuva model u `models/phishing_detector.pkl`
- cuva trening log u `outputs/training_*.log`

### 3) (Opcionalno) Lokalni test bez API-ja

```bash
python3 src/predictPhishing.py
```

Skripta koristi primer email teksta i vraca verovatnocu phishing klase.

### 4) Pokretanje API servera

```bash
python3 -m uvicorn src.api_server:app --reload --port 8000
```

Server koristi:

- model iz `models/phishing_detector.pkl`
- vectorizer iz `data/preprocessed_data.pkl`

Brza provera da server radi:

```bash
curl http://localhost:8000/health
```

Primer predikcije preko API-ja:

```bash
curl -X POST http://localhost:8000/predict \
	-H "Content-Type: application/json" \
	-d '{"text":"Hitno potvrdite nalog klikom na link"}'
```

Ocekivani oblik odgovora:

```json
{
	"prediction": 1,
	"probability": 0.9342
}
```

Napomena:

- `prediction = 1` znaci phishing
- `prediction = 0` znaci legit

## Firefox ekstenzija

Ekstenzija salje tekst trenutnog Gmail email-a na lokalni API (`http://localhost:8000/predict`).

### Ucitavanje ekstenzije (temporary)

1. Pokreni API server (korak iznad)
2. Otvori Firefox i idi na `about:debugging#/runtime/this-firefox`
3. Klikni `Load Temporary Add-on`
4. Izaberi fajl `extension/manifest.json`

### Koriscenje

1. Otvori Gmail poruku
2. Klikni ikonicu ekstenzije i dugme za analizu
3. Dobices rezultat `Phishing` ili `Legit` i verovatnocu (ako je dostupna)

Ekstenzija koristi:

- `extension/content.js`: cita tekst poruke iz Gmail DOM-a
- `extension/background.js`: prosledjuje tekst API-ju
- `extension/popup.js`: prikazuje rezultat u popup-u

## Kako radi model (ukratko)

- Ulaz: tekst email poruke
- Feature extraction: TF-IDF unigram + bigram
- Klasifikator: custom logistic regression
- Izlaz:
	- klasa (`0` legit, `1` phishing)
	- verovatnoca (`predict_proba`)


