# -*- coding: utf-8 -*-
"""Data Mining CODE.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1TDMwggJb8LnUynqxeVOoowPoDEuF1QWr
"""

# Mount Google Drive
from google.colab import drive
drive.mount('/content/drive')

# Core libraries
import os
import re
import string
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# NLP & text processing
# import nltk
# import spacy
# from collections import Counter
# from nltk.corpus import stopwords

"""#Pandas"""

# import pandas as pd

# file_path = "/content/drive/MyDrive/Big Data Project/df_combined_clean.csv"
# df = pd.read_csv(file_path)

# from imblearn.over_sampling import SMOTE
# import pandas as pd

# # 1. Choose user X
# user_X = "SallytheShizzle"

# # 2. Label the data
# df["label"] = df["user"].apply(lambda u: 1 if u == user_X else 0)

# df["label"].value_counts()

# # 3. Sample 10 positive + 10 negative for unseen set
# pos_sample = df[df["label"] == 1].sample(n=10, random_state=42)
# neg_sample = df[df["label"] == 0].sample(n=20, random_state=42)

# unseen_df = pd.concat([pos_sample, neg_sample], ignore_index=True)

# output_path = "/content/drive/MyDrive/Big Data Project/df_unseen.csv"
# unseen_df.to_csv(output_path, index=False)

# print(f"✅ DataFrame saved to: {output_path}")


# # 4. Remove unseen rows from main df (by index to avoid collision)
# df_filtered = df.drop(unseen_df.index)

# from imblearn.under_sampling import RandomUnderSampler
# from imblearn.over_sampling import SMOTE
# from sklearn.model_selection import train_test_split
# import pandas as pd
# import numpy as np

# # Separate features and label
# X = df.drop(columns=['label'])
# y = df['label']
# user_col = df['user']  # save user info

# # Keep only numeric features for resampling
# X_numeric = X.select_dtypes(include='number')

# # Step 1: Undersample class 0 to 250,000
# undersample = RandomUnderSampler(sampling_strategy={0: 250000, 1: y.sum()}, random_state=42)
# X_under, y_under = undersample.fit_resample(X_numeric, y)

# # Get user column after undersampling
# user_under = user_col.iloc[undersample.sample_indices_].reset_index(drop=True)

# # Step 2: SMOTE class 1 to 250,000
# smote = SMOTE(sampling_strategy={1: 250000}, random_state=42)
# X_balanced, y_balanced = smote.fit_resample(X_under, y_under)

# # Fix the user column after SMOTE
# # First get class 0 and class 1 user segments from undersampled data
# user_under = user_under.reset_index(drop=True)
# y_under = pd.Series(y_under).reset_index(drop=True)

# user_0 = user_under[y_under == 0].reset_index(drop=True)
# user_1 = user_under[y_under == 1].reset_index(drop=True)

# # Expand user_1 to match SMOTE upsampling
# user_1_balanced = pd.Series(
#     np.repeat(user_1.values, 250000 // len(user_1))
# ).reset_index(drop=True)

# # Combine user columns
# user_balanced = pd.concat([user_0, user_1_balanced], ignore_index=True)

# # Create final balanced DataFrame
# df_balanced = pd.DataFrame(X_balanced)
# df_balanced['user'] = user_balanced
# df_balanced['label'] = y_balanced

# # Confirm balance
# print("Balanced label counts:")
# print(df_balanced['label'].value_counts())

# df_balanced.to_csv("/content/drive/MyDrive/Big Data Project/df_balanced.csv", index=False)

# from sklearn.model_selection import train_test_split
# from sklearn.ensemble import RandomForestClassifier, VotingClassifier
# from xgboost import XGBClassifier
# from sklearn.metrics import classification_report, confusion_matrix

# # Step 1: Features and label
# X = df_balanced.drop(columns=['label', 'user'])  # Drop label and user
# y = df_balanced['label']

# # Step 2: Train-test split
# X_train, X_test, y_train, y_test = train_test_split(
#     X, y, test_size=0.2, random_state=42, stratify=y
# )

# # Check label distribution
# print("Train label distribution:")
# print(y_train.value_counts(normalize=True))

# print("\nTest label distribution:")
# print(y_test.value_counts(normalize=True))


# # Step 3: Define models
# xgb = XGBClassifier(use_label_encoder=False, eval_metric='logloss', random_state=42)
# rf = RandomForestClassifier(n_estimators=100, class_weight='balanced', random_state=42)

# # Step 4: Ensemble Voting Classifier
# ensemble = VotingClassifier(estimators=[
#     ('xgb', xgb),
#     ('rf', rf)
# ], voting='soft')  # 'soft' uses predicted probabilities

# # Step 5: Train
# ensemble.fit(X_train, y_train)

# # Step 6: Predict
# y_pred = ensemble.predict(X_test)

# # Step 7: Evaluation
# print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
# print("\nClassification Report:\n", classification_report(y_test, y_pred))

# from sklearn.model_selection import GridSearchCV

# xgb_param_grid = {
#     'n_estimators': [100, 200],
#     'max_depth': [3, 5, 7],
#     'learning_rate': [0.01, 0.1],
#     'subsample': [0.6, 0.8],
#     'colsample_bytree': [0.6, 0.8]
# }

# xgb_grid = GridSearchCV(
#     estimator=XGBClassifier(use_label_encoder=False, eval_metric='logloss', random_state=42),
#     param_grid=xgb_param_grid,
#     cv=3,
#     scoring='f1',
#     verbose=1,
#     n_jobs=-1
# )
# xgb_grid.fit(X_train, y_train)
# best_xgb = xgb_grid.best_estimator_

# rf_param_grid = {
#     'n_estimators': [100, 200],
#     'max_depth': [5, 10, None],
#     'min_samples_split': [2, 5],
#     'min_samples_leaf': [1, 2],
#     'bootstrap': [True, False]
# }

# rf_grid = GridSearchCV(
#     estimator=RandomForestClassifier(class_weight='balanced', random_state=42),
#     param_grid=rf_param_grid,
#     cv=3,
#     scoring='f1',
#     verbose=1,
#     n_jobs=-1
# )
# rf_grid.fit(X_train, y_train)
# best_rf = rf_grid.best_estimator_

# from sklearn.ensemble import VotingClassifier

# ensemble_tuned = VotingClassifier(estimators=[
#     ('xgb', best_xgb),
#     ('rf', best_rf)
# ], voting='soft')

# ensemble_tuned.fit(X_train, y_train)
# y_pred_unseen = ensemble_tuned.predict(X_unseen)
# print(confusion_matrix(y_unseen_true, y_pred_unseen))
# print(classification_report(y_unseen_true, y_pred_unseen))

# from sklearn.metrics import classification_report, confusion_matrix

# # Step 1: Load unseen dataset
# df_unseen = pd.read_csv("/content/drive/MyDrive/Big Data Project/df_unseen.csv")

# # Step 2: Separate features and label (if label exists)
# if 'label' in df_unseen.columns:
#     y_unseen_true = df_unseen['label']
# else:
#     raise ValueError("No 'label' column found in df_unseen for evaluation.")

# # Step 3: Prepare features (drop non-numerics and label)
# X_unseen = df_unseen.drop(columns=['user', 'label'], errors='ignore')
# X_unseen = X_unseen.select_dtypes(include='number')

# # Step 4: Predict
# y_unseen_pred = ensemble.predict(X_unseen)
# y_unseen_probs = ensemble.predict_proba(X_unseen)[:, 1]

# # Step 5: Attach predictions to dataframe
# df_unseen['predicted_label'] = y_unseen_pred
# df_unseen['predicted_proba_class1'] = y_unseen_probs

# # Step 6: Evaluate
# print("Confusion Matrix:\n", confusion_matrix(y_unseen_true, y_unseen_pred))
# print("\nClassification Report:\n", classification_report(y_unseen_true, y_unseen_pred))

"""#H2O

##Dependencies
"""

!pip install -f http://h2o-release.s3.amazonaws.com/h2o/latest_stable_Py.html h2o

import h2o
from h2o.grid.grid_search import H2OGridSearch
from h2o.estimators import H2OXGBoostEstimator, H2ORandomForestEstimator, H2OKMeansEstimator
from h2o.estimators.glm import H2OGeneralizedLinearEstimator
from h2o.estimators.deeplearning import H2ODeepLearningEstimator
from sklearn.metrics import confusion_matrix, classification_report
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

h2o.init()

"""##Loading the Data"""

# ✅ Load and split data
def load_data_to_h2o(path):
    hf = h2o.import_file(path)
    hf['label'] = hf['label'].asfactor()
    features = [col for col in hf.columns if col not in ['label', 'user']]
    target = 'label'
    train, test = hf.split_frame(ratios=[0.8], seed=42)
    return hf, train, test, features, target

hf, train, test, features, target = load_data_to_h2o("/content/drive/MyDrive/Big Data Project/df_balanced.csv")

"""## Modelling"""

def train_logistic_regression(train, features, target):
    from h2o.estimators.glm import H2OGeneralizedLinearEstimator
    model = H2OGeneralizedLinearEstimator(family='binomial', lambda_=0, standardize=True, solver='IRLSM', seed=42)
    model.train(x=features, y=target, training_frame=train)
    return model

def train_svm_like(train, features, target):
    from h2o.estimators.deeplearning import H2ODeepLearningEstimator
    model = H2ODeepLearningEstimator(hidden=[1], activation='Tanh', epochs=20,
                                     train_samples_per_iteration=-1, reproducible=True, seed=42)
    model.train(x=features, y=target, training_frame=train)
    return model

def train_xgboost(train, features, target):
    from h2o.estimators import H2OXGBoostEstimator

    xgb = H2OXGBoostEstimator(
        ntrees=200,
        max_depth=5,
        learn_rate=0.05,
        subsample=0.8,
        col_sample_rate=0.8,
        seed=42
    )
    xgb.train(x=features, y=target, training_frame=train)
    return xgb

def train_random_forest(train, features, target):
    from h2o.estimators import H2ORandomForestEstimator

    rf = H2ORandomForestEstimator(
        ntrees=100,
        max_depth=10,
        sample_rate=0.8,
        col_sample_rate_per_tree=0.8,
        seed=42
    )
    rf.train(x=features, y=target, training_frame=train)
    return rf

# 2. Train models
log_reg = train_logistic_regression(train, features, target)

svm_like = train_svm_like(train, features, target)

xgb = train_xgboost(train, features, target)

rf = train_random_forest(train, features, target)

"""## Evaluating Models"""

def evaluate_model(model, test_frame, model_name="Model"):
    print(f"\n\n===== {model_name} Evaluation =====")
    predictions = model.predict(test_frame).as_data_frame()['predict'].astype(int)
    true_labels = test_frame['label'].as_data_frame()['label'].astype(int)

    cm = confusion_matrix(true_labels, predictions)
    cr = classification_report(true_labels, predictions, digits=2)

    # Print classification report
    print("\nClassification Report:\n", cr)

    # Plot confusion matrix
    plt.figure(figsize=(6, 4))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
    plt.title(f'{model_name} - Confusion Matrix')
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    plt.show()

# 3. Evaluate on test set
evaluate_model(log_reg, test, "Logistic Regression")

evaluate_model(svm_like, test, "SVM-like")

evaluate_model(xgb, test, "XGBoost")

evaluate_model(rf, test, "Random Forest")

"""## Unseen Data"""

def evaluate_on_unseen(model, model_name="Model", unseen_path="/content/drive/MyDrive/Big Data Project/df_unseen.csv"):
    hf_unseen = h2o.import_file(unseen_path)
    if 'label' in hf_unseen.columns:
        hf_unseen['label'] = hf_unseen['label'].asfactor()

    evaluate_model(model, hf_unseen, model_name)

# 4. Evaluate on unseen
evaluate_on_unseen(log_reg, "Logistic Regression")

evaluate_on_unseen(svm_like, "SVM-like")

evaluate_on_unseen(xgb, "XGBoost")

evaluate_on_unseen(rf, "Random Forest")