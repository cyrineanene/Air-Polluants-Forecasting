import pandas as pd
from prophet import Prophet
import pickle
import matplotlib.pyplot as plt
import os

def train_and_save_model(data, country, pollutant, save_path="models"):
    os.makedirs(save_path, exist_ok=True)
    data['timestamp'] = pd.to_datetime(data['timestamp'])
    
    # Filtering the data for the specific country
    country_data = data[data['country'].str.upper() == country.upper()]
    # Preparing the data for Prophet
    df = country_data[['timestamp', pollutant]].rename(columns={'timestamp': 'ds', pollutant: 'y'})
    
    model = Prophet()
    model.fit(df)   
    model_file = os.path.join(save_path, f"{country}_{pollutant}_prophet_model.pkl")
    with open(model_file, 'wb') as f:
        pickle.dump(model, f)
    print(f"Model saved at: {model_file}")
    
def plot_predictions(forecast, title="Forecast"):
    # Extracting monthly predictions
    forecast['month'] = forecast['ds'].dt.to_period('M')
    monthly_forecast = forecast.groupby('month').mean(numeric_only=True).reset_index()
    monthly_forecast['month'] = monthly_forecast['month'].dt.strftime('%b %Y')  
    
    plt.figure(figsize=(10, 6))
    plt.plot(monthly_forecast['month'], monthly_forecast['yhat'], marker='o', label='Predicted Value', color='blue')
    plt.fill_between(
        monthly_forecast['month'],
        monthly_forecast['yhat_lower'],
        monthly_forecast['yhat_upper'],
        color='blue',
        alpha=0.2,
        label='Uncertainty Interval'
    )

    plt.xticks(rotation=45, fontsize=10)
    plt.yticks(fontsize=10)
    plt.xlabel("Month", fontsize=12)
    plt.ylabel("Predicted Value", fontsize=12)
    plt.title(title, fontsize=14)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.legend(fontsize=10)
    plt.tight_layout()
    plt.show()

def load_and_predict(model_file, periods=365):  
    with open(model_file, 'rb') as f:
        model = pickle.load(f)
    
    future = model.make_future_dataframe(periods=periods)
    forecast = model.predict(future)
    
    predictions_file = model_file.replace("_prophet_model.pkl", "_forecast.csv")
    forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].to_csv(predictions_file, index=False)
    print(f"Predictions saved to: {predictions_file}")

    plot_predictions(forecast)
    return predictions_file