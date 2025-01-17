import os

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder


# Function to train and save the vectorizer
def train_vectorizer(file_path, vectorizer_path='vectorizer.joblib'):
    """
    :return: Trained TfidfVectorizer
    """
    data = pd.read_csv(file_path)

    if data['Description'].isnull().sum() > 0:
        data['Description'].fillna('', inplace=True)

    vectorizer = TfidfVectorizer(max_features=500, stop_words='english')
    X_tfidf = vectorizer.fit_transform(data['Description'])

    joblib.dump(vectorizer, vectorizer_path)
    print(f"Vectorizer saved at {vectorizer_path}")

    return vectorizer


def process_uploaded_file(file, vectorizer_path='/Users/jojo/Downloads/Developer/spendalysis/backend/models/vectorizer.joblib'):
    print(f"Current working directory: {os.getcwd()}")

    df = pd.read_csv(file)

    required_columns = {"Date", "Description", "Amount"}
    if not required_columns.issubset(df.columns):
        raise ValueError("Invalid file format. Ensure columns: Date, Description, Amount.")

    if df['Description'].isnull().sum() > 0:
        df['Description'].fillna('', inplace=True)

    try:
        vectorizer = joblib.load(vectorizer_path)
    except Exception as e:
        raise ValueError(f"Error loading vectorizer: {e}")

    X_tfidf = vectorizer.transform(df['Description'])

    return df, X_tfidf


# Function to inspect feature names and IDF values (optional for debugging)
def print_vectorizer_details(vectorizer_path='vectorizer.joblib'):

    vectorizer = joblib.load(vectorizer_path)
    feature_names = vectorizer.get_feature_names_out()
    idf_values = vectorizer.idf_

    for feature, idf in zip(feature_names, idf_values):
        print(feature, ":", idf)

def label_encoder(data):
    d = pd.read_csv(data)
    encoder = LabelEncoder()
    d['encoded_category'] = encoder.fit_transform(d['Category'])
    joblib.dump(encoder, 'label_encoder.joblib')
    print(f"Categories: {encoder.classes_}")


def train_model(df ,vectorizer_path='/Users/jojo/Downloads/Developer/spendalysis/backend/models/vectorizer.joblib' ,
                encoder_path='/Users/jojo/Downloads/Developer/spendalysis/backend/models/label_encoder.joblib'):
    data = pd.read_csv(df)

    # Handle missing descriptions
    if data['Description'].isnull().sum() > 0:
        data['Description'].fillna('' ,inplace = True)

    try:
        # Load the vectorizer and transform the Description column
        vectorizer = joblib.load(vectorizer_path)
        X_tfidf = vectorizer.transform(data['Description'])
        X_tfidf_to_data_frame = pd.DataFrame(X_tfidf.toarray())

        # Convert TF-IDF column names to strings
        X_tfidf_to_data_frame.columns = X_tfidf_to_data_frame.columns.astype(str)

        # Combine TF-IDF features with the Amount column
        X = pd.concat([X_tfidf_to_data_frame ,data['Amount'].reset_index(drop = True).rename("Amount")] ,axis = 1)
        X.columns = X.columns.astype(str)  # Ensure all column names are strings

        # Load the encoder and encode the Category column
        encoder = joblib.load(encoder_path)
        data['encoded_category'] = encoder.transform(data['Category'])

        # Train the Random Forest Regressor
        model = RandomForestClassifier(n_estimators = 100 ,random_state = 42)
        X_train ,X_test ,y_train ,y_test = train_test_split(
            X ,data['encoded_category'] ,test_size = 0.2 ,random_state = 42
        )
        model.fit(X_train ,y_train)

        # Make predictions
        y_pred = model.predict(X_test)
        print("Predictions:" ,y_pred)
        print("Model trained successfully!")

        # Save the trained model
        joblib.dump(model ,'expense_classifier.joblib')

    except Exception as e:
        print("Error during training:" ,e)


if __name__ == '__main__':
    vec_trained = train_vectorizer("../data/finance.csv" ,vectorizer_path = 'vectorizer.joblib')

    # Step 2: (Optional) Inspect vectorizer details
    print_vectorizer_details(vectorizer_path = 'vectorizer.joblib')

    label_encoder("../data/finance.csv")
    train_model("../data/finance.csv")