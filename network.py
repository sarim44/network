import random
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

def generate_network_data(num_samples=1000):
    data = {
        'packet_drops': [random.randint(0, 100) for _ in range(num_samples)],
        'latency': [random.uniform(0.1, 1.0) for _ in range(num_samples)],
        'failure': [random.randint(0, 1) for _ in range(num_samples)]
    }
    return pd.DataFrame(data)

def train_network_model(df):
    X = df[['packet_drops', 'latency']]
    y = df['failure']
    model = RandomForestClassifier()
    model.fit(X, y)
    return model

def predict_network_status(model, packet_drops, latency):
    new_data = pd.DataFrame({'packet_drops': [packet_drops], 'latency': [latency]})
    prediction = model.predict(new_data)
    return "Failure" if prediction == 1 else "Operational"

def main():
    network_df = generate_network_data()
    network_df.to_csv('network_data.csv', index=False)
    model = train_network_model(network_df)

    # Example Prediction
    status = predict_network_status(model, 20, 0.5)
    print("Predicted Network Status:", status)

if __name__ == "__main__":
    main()
