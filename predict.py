import joblib
import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
# CRITICAL: This line is essential for the predict_email function to work.
from preprocess import process_single_email 

model = load_model("models/phishing_model.keras")
tokenizer = joblib.load("models/tokenizer.pkl")
scaler = joblib.load("models/url_scaler.pkl")
feature_columns = joblib.load("models/url_feature_columns.pkl")
max_len = 300

# The rest of the functions from preprocess.py (clean_text, extract_first_url, etc.)
# MUST be available within preprocess.py for process_single_email to work.

def predict_email(email_text, threshold=0.5):
    
    # This calls the function imported from preprocess.py
    clean_text, url_features_dict = process_single_email(email_text) 

    # 1. Prepare Text Input (LSTM Branch)
    text_seq = tokenizer.texts_to_sequences([clean_text])
    text_pad = pad_sequences(text_seq, maxlen=max_len)

    # 2. Prepare Numerical Input (Dense Branch)
    url_features_df = pd.DataFrame([url_features_dict])
    url_features_df = url_features_df.reindex(columns=feature_columns, fill_value=0)
    url_features_scaled = scaler.transform(url_features_df) 
        
    # 3. Predict
    raw_score = model.predict([text_pad, url_features_scaled], verbose=0)[0][0]
    
    # Label Inversion Fix
    score = 1.0 - raw_score
    
    label = "Phishing" if score >= threshold else "Legitimate"
        

    return score, label


