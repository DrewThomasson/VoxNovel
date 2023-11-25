import os
import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from nltk.tokenize import sent_tokenize, word_tokenize

# Define the function to extract features from a paragraph
def extract_features(paragraph):
    sentences = sent_tokenize(paragraph)
    words = word_tokenize(paragraph)
    features = {
        "num_sentences": len(sentences),
        "num_words": len(words),
        "presence_parentheses": 1 if "(" in paragraph or ")" in paragraph else 0,
        "presence_dash": 1 if "-" in paragraph else 0,
        "presence_semicolon_colon": 1 if ";" in paragraph or ":" in paragraph else 0,
        "presence_question_mark": 1 if "?" in paragraph else 0,
        "presence_apostrophe": 1 if "'" in paragraph else 0,
        "std_sentence_length": np.std([len(sent) for sent in sentences]),
        "mean_diff_sentence_length": np.mean([abs(len(sentences[i]) - len(sentences[i-1])) 
                                              for i in range(1, len(sentences))]) if len(sentences) > 1 else 0,
        "presence_short_sentences": 1 if any(len(sent) < 11 for sent in sentences) else 0,
        "presence_long_sentences": 1 if any(len(sent) > 34 for sent in sentences) else 0,
        "presence_numbers": 1 if any(char.isdigit() for char in paragraph) else 0,
        "presence_more_capitals": 1 if sum(1 for c in paragraph if c.isupper()) > paragraph.count('.') * 2 else 0,
        "presence_although": 1 if "although" in words else 0,
        "presence_however": 1 if "however" in words else 0,
        "presence_but": 1 if "but" in words else 0,
        "presence_because": 1 if "because" in words else 0,
        "presence_this": 1 if "this" in words else 0,
        "presence_others_researchers": 1 if "others" in words or "researchers" in words else 0,
        "presence_et": 1 if "et" in words else 0
    }
    return features

# Function to process all files in a given directory and extract features
def process_files_in_directory(directory, label):
    features_list = []
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            file_path = os.path.join(directory, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
                # Assuming each file contains one paragraph for simplicity
                features = extract_features(text)
                features['label'] = label
                features_list.append(features)
    return features_list

# Process files and create a DataFrame
gpt_features = process_files_in_directory('gpt', 1)  # Label 1 for gpt
human_features = process_files_in_directory('human', 0)  # Label 0 for human
print(len(human_features))
print(human_features)
# Combine features into a single DataFrame
combined_features = gpt_features + human_features
df = pd.DataFrame(combined_features)

# Split into features and target
X = df.drop('label', axis=1)
y = df['label']

# Split the dataset into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
# Train the XGBoost classifier
model = xgb.XGBClassifier(use_label_encoder=False, eval_metric='logloss')
model.fit(X_train, y_train)

# Predict the labels for the test set
y_pred = model.predict(X_test)
# Calculate the accuracy of the model
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy * 100:.2f}%")

# The model is now trained and can be used to predict whether a new paragraph is written by ChatGPT or a human.
# If you need to process new data, you would extract the features using the extract_features function and then use model.predict() to get the predictions.
