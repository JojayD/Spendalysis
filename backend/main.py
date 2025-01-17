from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import joblib
import pandas as pd
import os
import numpy as np

vectorizer = joblib.load("/Users/jojo/Downloads/Developer/spendalysis/backend/models/vectorizer.joblib")
model = joblib.load("/Users/jojo/Downloads/Developer/spendalysis/backend/models/expense_classifier.joblib")
encoder = joblib.load("/Users/jojo/Downloads/Developer/spendalysis/backend/models/label_encoder.joblib")

UPLOAD_DIR = "uploaded_files"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

app = FastAPI()
origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def debug_print_features(df, X_tfidf_df, X_final=None):
    """Helper function to print detailed feature information"""
    print("\n=== DEBUG INFORMATION ===")
    print(f"DataFrame head:\n{df.head()}")
    print(f"\nDataFrame columns: {df.columns.tolist()}")
    print(f"DataFrame shape: {df.shape}")

    print(f"\nVectorizer vocabulary size: {len(vectorizer.vocabulary_)}")
    print(f"Vectorizer feature names: {vectorizer.get_feature_names_out()}")

    print(f"\nTF-IDF DataFrame shape: {X_tfidf_df.shape}")
    print(f"TF-IDF columns: {X_tfidf_df.columns.tolist()[:5]}... (showing first 5)")

    if X_final is not None:
        print(f"\nFinal feature matrix shape: {X_final.shape}")
        print(f"Final feature columns: {X_final.columns.tolist()}")
        print(f"Model expected features: {model.n_features_in_}")

        # Check for NaN values
        print(f"\nNaN values in final features: {X_final.isna().sum().sum()}")

        # Print some basic stats about the Amount column
        if 'Amount' in df.columns:
            print(f"\nAmount column statistics:")
            print(df['Amount'].describe())

@app.post("/upload")
async def upload_file_predict_data(file: UploadFile = File(...)):
    file_path = None
    try:
        # Save uploaded file
        os.makedirs("uploaded_files", exist_ok=True)
        content = await file.read()
        file_path = f"uploaded_files/{file.filename}"
        with open(file_path, "wb") as f:
            f.write(content)

        print(f"\nProcessing file: {file.filename}")

        # Read the CSV file
        df = pd.read_csv(file_path)
        print(f"\nOriginal DataFrame columns: {df.columns.tolist()}")

        # Validate required columns
        required_columns = {"Date", "Description", "Amount"}
        if not required_columns.issubset(df.columns):
            raise ValueError(f"Missing columns. Required: {required_columns}, Got: {set(df.columns)}")

        # Handle missing descriptions
        null_descriptions = df['Description'].isnull().sum()
        print(f"\nNull descriptions found: {null_descriptions}")
        df['Description'].fillna('', inplace=True)

        # Transform descriptions using TF-IDF
        print("\nApplying TF-IDF transformation...")
        X_tfidf = vectorizer.transform(df['Description'])
        X_tfidf_df = pd.DataFrame(X_tfidf.toarray())
        X_tfidf_df.columns = X_tfidf_df.columns.astype(str)

        # Add Amount column to features
        print("\nAdding Amount column to features...")
        X = pd.concat([X_tfidf_df, df['Amount'].reset_index(drop=True)], axis=1)
        X.columns = X.columns.astype(str)

        # Print detailed debug information
        debug_print_features(df, X_tfidf_df, X)

        # Additional model information
        print("\n=== MODEL INFORMATION ===")
        if hasattr(model, 'feature_names_in_'):
            print(f"Model's feature names: {model.feature_names_in_}")
        print(f"Model's n_features_in_: {model.n_features_in_}")

        # Predict categories
        print("\nMaking predictions...")
        predictions = model.predict(X)
        df["Predicted_Category"] = encoder.inverse_transform(predictions)

        # Clean up uploaded file
        os.remove(file_path)

        return JSONResponse(content=df.to_dict(orient="records"))

    except Exception as e:
        print(f"\nERROR: {str(e)}")
        print(f"Error type: {type(e)}")
        import traceback
        print(f"Traceback:\n{traceback.format_exc()}")

        # Clean up uploaded file in case of error
        if file_path and os.path.exists(file_path):
            os.remove(file_path)
        return JSONResponse(
            content={
                "error": str(e),
                "error_type": str(type(e)),
                "traceback": traceback.format_exc()
            },
            status_code=500
        )