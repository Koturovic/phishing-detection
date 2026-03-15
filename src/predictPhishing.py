import joblib

def predict_email(model_file, vectorizer_file, email_text):
    model = joblib.load(model_file)
    _, _, vectorizer = joblib.load(vectorizer_file)
    email_vector = vectorizer.transform([email_text]).toarray()
    prediction = model.predict(email_vector)
    return model.predict_proba(email_vector)  # Return probability of being phishing

if __name__ == "__main__":
    email_text = "Obaveštavamo Vas. Hitno: KYC verifikacija nije završena. Rok 10 minuta. Popunite bezbednosni upitnik na priloženom linku. Iznos: 1.990 RSD. Zahtev ističe za 60 minuta od prijema poruke. Kod: 19317994."
    #email_text = "Primili smo zahtev za resetovanje lozinke za vas nalog na platformi Edukacija; ukoliko niste vi poslali ovaj zahtev, slobodno zanemarite ovaj mejl, a vasa lozinka ce ostati nepromenjena."
    #email_text = "Poštovane koleginice i kolege, Raspored odbrane projekta je u prilogu. Možete se menjati ali neophodno je da javite zamenu termina mejlom. "
    #email_text = "Upozorenje banke: ALARM: Primećen je neuobičajen pokušaj prijave na Vaš nalog. Ako ovo niste bili Vi, molimo Vas da odmah obezbedite svoj nalog na: http://bank-security-alert.com/."
    result = predict_email("models/phishing_detector.pkl", "data/preprocessed_data.pkl", email_text)
    print(f"Prediction: {result}")