import os
import pandas as pd
import json
import matplotlib.pyplot as plt
from src.model import train_and_save_model, load_and_predict, plot_predictions
from utils import calculate_aqi, plot_all_forecasts, plot_global_aqi

data = pd.read_csv("src\data\cleaned_dataset.csv")

country = 'andorra'
pollutants = ['no2', 'o3', 'so2', 'pm2_5', 'pm10']

pollutant_aqi_values = {}
all_forecasts = {}
monthly_aqi_data = {}

#Step 1: Calculate the AQI For each month and each pollutant
for pollutant in pollutants:
    train_and_save_model(data, country, pollutant)

    #Load saved model
    model_file = f"models/{country}_{pollutant}_prophet_model.pkl"
    if os.path.exists(model_file):
        forecast = load_and_predict(model_file, 356)
        all_forecasts[pollutant] = forecast
        
        #Calculate the AQI for each pollutant for each month
        forecast_df = pd.DataFrame(forecast)
        forecast_df['month'] = forecast_df['ds'].dt.to_period('M')
        monthly_forecast = forecast_df.groupby('month')['yhat'].mean().reset_index()
        monthly_forecast['AQI'] = monthly_forecast['yhat'].apply(lambda x: calculate_aqi(pollutant, x))
        #Save the monthly AQI results in a CSV File 
        aqi_file = os.path.join('results', f"{country}_{pollutant}_monthly_forecast_aqi.csv")
        monthly_forecast.to_csv(aqi_file, index=False)
        print(f"Monthly AQI data saved to: {aqi_file}")
        
        #Save the maximum for each AQI and adding it to the rest of the pollutants
        monthly_aqi_data[pollutant] = monthly_forecast[['month', 'AQI']].set_index('month')
        pollutant_aqi_values[pollutant] = monthly_forecast['AQI'].max()

    else:
        print(f"Model file for {pollutant} not found. Please train the model first.")

#Step 2: Calculate the Global AQI for each month
global_aqi_df = pd.concat(monthly_aqi_data.values(), axis=1)
global_aqi_df.columns = pollutants

global_aqi_df['Global_AQI'] = global_aqi_df.max(axis=1)

global_aqi_file = os.path.join('results', f"{country}_global_monthly_aqi.csv")
global_aqi_df.to_csv(global_aqi_file, index=True)
print(f"Global AQI data saved to: {global_aqi_file}")

#Step 3: Plotting all the forecast values then the Global AQI
plot_all_forecasts(all_forecasts, country)
plot_global_aqi(global_aqi_df)