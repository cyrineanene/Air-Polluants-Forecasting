import os
import pandas as pd
import json
import matplotlib.pyplot as plt
from src.model import train_and_save_model, load_and_predict, plot_predictions
from utils import calculate_aqi, plot_all_forecasts

data = pd.read_csv("data\\air_quality_data_all_countries.csv")

# Input country name
country = 'andorra'
#country = input("Enter the country: ")
pollutants = ['co', 'no', 'no2', 'o3', 'so2', 'pm2_5', 'pm10', 'nh3']

pollutant_aqi_values = {}
all_forecasts = {}

# Forecast and plot for each pollutant
for pollutant in pollutants:
    train_and_save_model(data, country, pollutant)

    # Load saved model
    model_file = f"models/{country}_{pollutant}_prophet_model.pkl"
    if os.path.exists(model_file):
        forecast = load_and_predict(model_file, 356)
        all_forecasts[pollutant] = forecast
        
        #calculating the AQI for each pollutant for each month 
        forecast_df = pd.DataFrame(forecast)
       
        forecast_df['month'] = forecast_df['ds'].dt.to_period('M')
        monthly_forecast = forecast_df.groupby('month')['yhat'].mean().reset_index()
        
        monthly_forecast['AQI'] = monthly_forecast['yhat'].apply(lambda x: calculate_aqi(pollutant, x))
        
        aqi_file = os.path.join('results', f"{country}_{pollutant}_monthly_forecast_aqi.csv")
        monthly_forecast.to_csv(aqi_file, index=False)
        print(f"Monthly AQI data saved to: {aqi_file}")

        #storing the maximum AQI value for the pollutant used later to calculate the AQI Global
        pollutant_aqi_values[pollutant] = monthly_forecast['AQI'].max()
        
        # forecast_df = pd.DataFrame(forecast)
        # forecast_df['AQI'] = forecast_df['yhat'].apply(lambda x: calculate_aqi(pollutant, x))
        # pollutant_aqi_values[pollutant] = forecast_df['AQI'].dropna().max()

    else:
        print(f"Model file for {pollutant} not found. Please train the model first.")


# Plot forecasts in a single window
plot_all_forecasts(all_forecasts, country)

# Save AQI results to JSON
# aqi_file = f"results/{country}_aqi_results.json"
# with open(aqi_file, 'w') as f:
#     json.dump(pollutant_aqi_values, f, indent=4)
# print(f"AQI results saved to: {aqi_file}")

# # Plot AQI values
# plt.figure(figsize=(10, 6))
# plt.bar(pollutant_aqi_values.keys(), pollutant_aqi_values.values(), color='skyblue')
# plt.xlabel("Pollutants", fontsize=12)
# plt.ylabel("AQI", fontsize=12)
# plt.title(f"AQI Values for {country}", fontsize=14)
# plt.grid(axis='y', linestyle='--', alpha=0.7)
# plt.tight_layout()
# plt.show()

# # Calculate and plot global AQI
# global_aqi = max(pollutant_aqi_values.values())
# print("\nGlobal AQI Value:")
# print(global_aqi)