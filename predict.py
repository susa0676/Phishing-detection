import joblib
import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import time, psutil, os, logging
logging.basicConfig(level=logging.INFO)
def log_state(tag=""):
    proc = psutil.Process(os.getpid())
    logging.info(f"{tag} | pid={os.getpid()} rss_mb={proc.memory_info().rss/1024/1024:.1f}")

# CRITICAL: This line is essential for the predict_email function to work.
from preprocess import process_single_email 

og_state("startup begin")
model = load_model("models/phishing_model.keras")
tokenizer = joblib.load("models/tokenizer.pkl")
scaler = joblib.load("models/url_scaler.pkl")
# warm up: tiny fake input (same shapes)
_dummy_text = pad_sequences([[1,2,3]], maxlen=300)
_dummy_num = scaler.transform(np.zeros((1, len(joblib.load("models/url_feature_columns.pkl")))))
_ = model.predict([_dummy_text, _dummy_num], verbose=0)
log_state("startup done - warmed up model")
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

