import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score, KFold
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
import numpy as np

def load_data(file_path):
    return pd.read_csv(file_path)

def calculate_moving_average(df, column, window=3):
        return df[column].rolling(window=window).mean().iloc[-1]

if __name__ == "__main__":
    
    haaland_data_path = '../data/processed/Haaland_stats.csv'

    haaland_data = load_data(haaland_data_path)
    
    haaland_df = pd.concat([haaland_data], ignore_index=True)
    
    haaland_df.fillna(0, inplace=True)


    features = ['Age', 'Min', 'Gls', 'xG', 'npxG', 'Sh', 'SoT', 'xAG', 'G/SoT', 'G/Sh', 'SoT%', 'Dist', 'FK', 'PK']
    X = haaland_df[features]
    Y = haaland_df['xG']

    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

    model = LinearRegression()
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    mse = mean_squared_error(y_test, y_pred)
    print("Mean Squared Error: ", mse)


    next_season_data = pd.DataFrame({
    'Age': [24],  
    'Min': calculate_moving_average(haaland_df, 'Min'),
    'Gls': calculate_moving_average(haaland_df, 'Gls'),
    'xG': calculate_moving_average(haaland_df, 'xG'),
    'npxG': calculate_moving_average(haaland_df, 'npxG'),
    'Sh': calculate_moving_average(haaland_df, 'Sh'),
    'SoT': calculate_moving_average(haaland_df, 'SoT'),
    'xAG': calculate_moving_average(haaland_df, 'xAG'),
    'G/SoT': calculate_moving_average(haaland_df, 'G/SoT'),
    'G/Sh': calculate_moving_average(haaland_df, 'G/Sh'),
    'SoT%': calculate_moving_average(haaland_df, 'SoT%'),
    'Dist': calculate_moving_average(haaland_df, 'Dist'),
    'FK': calculate_moving_average(haaland_df, 'FK'),
    'PK': calculate_moving_average(haaland_df, 'PK')
    })
    print(next_season_data)


    next_season_xG = model.predict(next_season_data)
    print("Predicted xG for next season:", next_season_xG)