from src.model import train_and_save_model, load_and_predict
import os
import pandas as pd

data = pd.read_csv("data\\air_quality_data_all_countries.csv")
    
country = input("Enter the country: ")
pollutant = input("Enter the pollutant (co, no, no2, o3, so2, pm2_5, pm10, nh3): ")

train_and_save_model(data, country, pollutant)

#Load the saved model     
model_file = f"models/{country}_{pollutant}_prophet_model.pkl"
#Make the prediction
if os.path.exists(model_file):
    load_and_predict(model_file, 356)  #extending the values 36 steps beyond the existing data 
else:
    print("Model file not found. Please train the model first.")