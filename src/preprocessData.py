import pandas as pd # manipulate data
from sklearn.feature_extraction.text import TfidfVectorizer # Term Frequency-Inverse Document Frequency (TF-IDF) vectorizer
import joblib # save and load trained model





def preprocess_data(input_file, output_file):

    # Load the dataset
    data = pd.read_csv(input_file)

    # Preprocess the text data using TF-IDF vectorization
    vectorizer = TfidfVectorizer(max_features=5000, ngram_range=(1, 2))
    X = vectorizer.fit_transform(data['text']).toarray()
    y = data['label'].values
    joblib.dump((X, y, vectorizer), output_file)

    print(f"Preprocessed data saved to {output_file}")

if __name__ == "__main__":
    preprocess_data("data/phishing_emails.csv", "data/preprocessed_data.pkl")



# Explanation:


# 1. Libiaries:

# Term frequency -> how many times a term appears in a document
# Inverse document frequency -> how important a term is across all documents


# 2. Preprocess data:
# max_features=5000 -> limit the number of features to 5000
# ngram_range=(1, 2):
#                    1 -> unigrams (single words)  'bank'
#                    2 -> bigrams (pairs of consecutive words) - 'verify account'
#  
# X = vectorizer.fit_transform(data['text']).toarray() -> fit the vectorizer to the text data and transform it into a numerical array


# 3. Save preprocessed data:
# joblib.dump((X, y, vectorizer), output_file) -> save the pre





