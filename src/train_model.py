import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score, KFold
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
import numpy as np

def load_data(file_path):
    return pd.read_csv(file_path)


if __name__ == "__main__":
    all_player_path = '../data/processed/player_shooting_2023_2024.csv'
    all_player_data = load_data(all_player_path)
    haaland_data_path = '../data/processed/Haaland_stats.csv'
    haaland_data = load_data(haaland_data_path)

    similar_players_path = [
        '../data/processed/Dovbyk_stats.csv',
        '../data/processed/Joselu_stats.csv',
        '../data/processed/Kane_stats.csv',
        '../data/processed/Osimhen_stats.csv',
        '../data/processed/Vlahovic_stats.csv'
    ]

    similar_players_data = pd.concat([load_data(file) for file in similar_players_path], ignore_index=True)
    combined_data = pd.concat([haaland_data, similar_players_data, all_player_data], ignore_index=True)


    feature_cols = ['Gls', 'Gls/90', 'Sh', 'SoT', 'SoT%', 'Sh/90', 'SoT/90', 'G/Sh', 'G/SoT']
    target_col = 'xG'

    X = combined_data[feature_cols]
    Y = combined_data[target_col]

    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

    print(f"Training set size: {X_train.shape[0]}")
    print(f"Testing set size: {X_test.shape[0]}")
    
    model = LinearRegression()

    kf = KFold(n_splits=5, shuffle=True, random_state=42)
    mse_scores = cross_val_score(model, X_train, y_train, scoring='neg_mean_squared_error', cv=kf)
    r2_scores = cross_val_score(model, X_train, y_train, scoring='r2', cv=kf)

