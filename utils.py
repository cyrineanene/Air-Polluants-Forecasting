def calculate_aqi(pollutant, value):
    aqi_breakpoints = {
        'co': [(0, 4.4, 0, 50), (4.5, 9.4, 51, 100), (9.5, 12.4, 101, 150), (12.5, 15.4, 151, 200)],
        'no2': [(0, 53, 0, 50), (54, 100, 51, 100), (101, 360, 101, 150), (361, 649, 151, 200)],
        'o3': [(0, 54, 0, 50), (55, 70, 51, 100), (71, 85, 101, 150), (86, 105, 151, 200)],
        'so2': [(0, 35, 0, 50), (36, 75, 51, 100), (76, 185, 101, 150), (186, 304, 151, 200)],
        'pm2_5': [(0, 12, 0, 50), (12.1, 35.4, 51, 100), (35.5, 55.4, 101, 150), (55.5, 150.4, 151, 200)],
        'pm10': [(0, 54, 0, 50), (55, 154, 51, 100), (155, 254, 101, 150), (255, 354, 151, 200)],
        'nh3': [(0, 200, 0, 50), (201, 400, 51, 100), (401, 800, 101, 150), (801, 1200, 151, 200)],
    }

    breakpoints = aqi_breakpoints.get(pollutant, [])
    for bp in breakpoints:
        if bp[0] <= value <= bp[1]:
            return (bp[3] - bp[2]) / (bp[1] - bp[0]) * (value - bp[0]) + bp[2]
    return None

def plot_all_forecasts(all_forecasts, country):
    import itertools
    import matplotlib.pyplot as plt
    colors = itertools.cycle(['blue', 'green', 'red', 'orange', 'purple', 'brown', 'pink', 'cyan'])

    plt.figure(figsize=(12, 8))

    for pollutant, forecast in all_forecasts.items():
        
        forecast['month'] = forecast['ds'].dt.to_period('M')
        monthly_forecast = forecast.groupby('month').mean(numeric_only=True).reset_index()
        monthly_forecast['month'] = monthly_forecast['month'].dt.strftime('%b %Y') 

        color = next(colors)

        plt.plot(monthly_forecast['month'], monthly_forecast['yhat'], marker='o', label=f'{pollutant} - Predicted', linestyle='-', color=color)
        plt.fill_between(
            monthly_forecast['month'],
            monthly_forecast['yhat_lower'],
            monthly_forecast['yhat_upper'],
            color=color, alpha=0.2
        )

    plt.xticks(rotation=45, fontsize=10)
    plt.yticks(fontsize=10)
    plt.xlabel("Month", fontsize=12)
    plt.ylabel("Predicted Value", fontsize=12)
    plt.title(f"Forecast Predictions for {country}", fontsize=14)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.legend(fontsize=10)
    plt.tight_layout()
    plt.show()