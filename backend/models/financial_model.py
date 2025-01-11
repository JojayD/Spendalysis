import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib

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


def process_uploaded_file(file, vectorizer_path='vectorizer.joblib'):
	df = pd.read_csv(file)

	required_columns = {"Date", "Description", "Amount"}
	if not required_columns.issubset(df.columns):
		raise ValueError("Invalid file format. Ensure columns: Date, Description, Amount.")

	if df['Description'].isnull().sum() > 0:
		df['Description'].fillna('', inplace=True)

	vectorizer = joblib.load(vectorizer_path)

	X_tfidf = vectorizer.transform(df['Description'])

	return df, X_tfidf


# Function to inspect feature names and IDF values (optional for debugging)
def print_vectorizer_details(vectorizer_path='vectorizer.joblib'):

	vectorizer = joblib.load(vectorizer_path)
	feature_names = vectorizer.get_feature_names_out()
	idf_values = vectorizer.idf_

	for feature, idf in zip(feature_names, idf_values):
		print(feature, ":", idf)


if __name__ == '__main__':
	vec_trained = train_vectorizer("../data/finance.csv" ,vectorizer_path = 'vectorizer.joblib')

	# Step 2: (Optional) Inspect vectorizer details
	print_vectorizer_details(vectorizer_path = 'vectorizer.joblib')

