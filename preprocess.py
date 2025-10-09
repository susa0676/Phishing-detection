import pandas as pd
import re
import tldextract
from sklearn.preprocessing import LabelEncoder
import numpy as np

# 1. Clean email body text
def clean_text(text):
    text = str(text).lower()
    text = re.sub(r'\n', ' ', text)
    text = re.sub(r'[^a-z0-9\s:/.-<>?=&]', '', text)
    return re.sub(r'\s+', ' ', text).strip()

# 2. Extract the first URL from the mail
def extract_first_url(text):
    urls = re.findall(r'https?://[^\s]+', str(text))
    return urls[0] if urls else ''

# 3. Extract URL features
def extract_url_features(url):
    if not url:
        return {
            'url_length': 0, 'has_https': 0, 'num_dots': 0, 'num_hyphens': 0, 
            'has_at': 0, 'has_ip': 0, 'is_shortened': 0, 'has_suspicious_kw': 0, 
            'uncommon_tld': 0, 'domain_length': 0
        }
    
    features = {}
    features['url_length'] = len(url)
    features['has_https'] = int(url.startswith('https'))
    features['num_dots'] = url.count('.')
    features['num_hyphens'] = url.count('-')
    features['has_at'] = int('@' in url)
    
    ip_pattern = r'https?://\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
    features['has_ip'] = int(bool(re.match(ip_pattern, url)))

    domain_info = tldextract.extract(url)
    domain = domain_info.domain
    suffix = domain_info.suffix

    shorteners = ['bit', 'tinyurl', 'ow', 't', 'is', 'goo', 'rebrandly', 'url']
    features['is_shortened'] = int(domain in shorteners)

    suspicious_keywords = ['login', 'verify', 'update', 'secure', 'bank', 'account', 'paypal']
    features['has_suspicious_kw'] = int(any(kw in url.lower() for kw in suspicious_keywords))

    uncommon_tlds = ['xyz', 'top', 'club', 'info', 'support', 'tk', 'ml', 'cf', 'ga']
    features['uncommon_tld'] = int(suffix in uncommon_tlds)

    features['domain_length'] = len(domain)

    return features

# 4. Extract text-based features
def extract_text_features(text):
    features = {}
    
    phishing_keywords = ['verify', 'account', 'password', 'urgent', 'suspended', 
                         'click', 'free', 'prize', 'congratulations', 'limited', 
                         'paypal', 'bank', 'update', 'secure', 'login',
                         'payroll', 'tax', 'errors', 'confidential', 'submission'] 
    
    legit_keywords = ['meeting', 'project', 'schedule', 'update', 'invoice', 
                      'team', 'thanks', 'report', 'office', 'zoom']

    features['phish_kw_count'] = sum(text.count(kw) for kw in phishing_keywords)
    features['legit_kw_count'] = sum(text.count(kw) for kw in legit_keywords)

    return features

def get_processed_data(csv_path):
    df = pd.read_csv(csv_path)
    if 'Unnamed: 0' in df.columns:
        df = df.drop(columns=['Unnamed: 0'])

    df.columns = ['email_text', 'email_type']

    label_encoder = LabelEncoder()
    df['label'] = label_encoder.fit_transform(df['email_type'])

    df['clean_text'] = df['email_text'].apply(clean_text) 
    df['url'] = df['email_text'].apply(extract_first_url)

    url_features_df = df['url'].apply(extract_url_features).apply(pd.Series)
    text_features_df = df['clean_text'].apply(extract_text_features).apply(pd.Series)

    combined_features_df = pd.concat([url_features_df, text_features_df], axis=1)

    # DANGER AMPLIFIER: Phish_kw_count * (Suspicious_kw + Uncommon_TLD)
    url_suspicion_score = combined_features_df['has_suspicious_kw'] + combined_features_df['uncommon_tld']
    combined_features_df['lure_url_interaction'] = combined_features_df['phish_kw_count'] * url_suspicion_score
    
    # SAFETY AMPLIFIER (NEW): Legitimate reward * (1 - Suspicion Score)
    # This prevents the False Positive (Email J) by strongly rewarding safe context.
    combined_features_df['safety_amplifier'] = combined_features_df['legit_kw_count'] * (1 - url_suspicion_score)

    return df['clean_text'].tolist(), combined_features_df, df['label'].values

# For single prediction
def process_single_email(email_text):
    clean = clean_text(email_text)
    url = extract_first_url(email_text)
    
    url_features = extract_url_features(url)
    text_features = extract_text_features(clean)
    
    # Calculate the DANGER Interaction Term
    url_suspicion_score = url_features['has_suspicious_kw'] + url_features['uncommon_tld']
    lure_url_interaction = text_features['phish_kw_count'] * url_suspicion_score
    
    # Calculate the SAFETY Interaction Term
    safety_amplifier = text_features['legit_kw_count'] * (1 - url_suspicion_score)
    
    # Final combined features (14 features total)
    combined_features = {**url_features, **text_features, 
                         'lure_url_interaction': lure_url_interaction,
                         'safety_amplifier': safety_amplifier}
    
    return clean, combined_features