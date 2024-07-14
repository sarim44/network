import sqlite3
import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np

def setup_database():
    conn = sqlite3.connect('it_assets.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS assets (
        id INTEGER PRIMARY KEY,
        name TEXT,
        usage_hours INTEGER,
        last_maintenance DATE,
        lifecycle_stage TEXT
    )''')
    conn.commit()
    return conn, cursor

def insert_example_data(cursor):
    assets = [
        ('Server A', 1000, '2024-01-01', 'Operational'),
        ('Server B', 2000, '2023-12-01', 'Operational')
    ]
    cursor.executemany('INSERT INTO assets (name, usage_hours, last_maintenance, lifecycle_stage) VALUES (?, ?, ?, ?)', assets)

def retrieve_data(conn):
    df = pd.read_sql_query('SELECT * FROM assets', conn)
    return df

def train_model(df):
    X = df['usage_hours'].values.reshape(-1, 1)
    y = np.where(df['lifecycle_stage'] == 'Operational', 0, 1)
    model = LinearRegression()
    model.fit(X, y)
    return model

def predict_lifecycle(model, usage_hours):
    prediction = model.predict(np.array([[usage_hours]]))
    return "Operational" if prediction < 0.5 else "Needs Maintenance"

def main():
    conn, cursor = setup_database()
    insert_example_data(cursor)
    conn.commit()
    df = retrieve_data(conn)
    model = train_model(df)
    conn.close()

    # Example Prediction
    prediction = predict_lifecycle(model, 1500)
    print("Predicted Lifecycle Stage:", prediction)

if __name__ == "__main__":
    main()
