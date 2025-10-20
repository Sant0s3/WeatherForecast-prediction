# WeatherPredict AI

**WeatherPredict AI** is a Python project that predicts weather temperatures (min, max, current, and feels-like) for Cairo based on input weather parameters. It uses a **Random Forest Regressor** with preprocessing pipelines for numerical and categorical features.

---

## Features

- Predicts:
  - Minimum Temperature (`tempmin`)
  - Maximum Temperature (`tempmax`)
  - Current Temperature (`temp`)
  - Feels Like Temperature (`feelslike`)
- Input parameters:
  - Wind Speed (`windspeed`) in km/h
  - Wind Direction (`winddir`) in degrees
  - Sea Level Pressure (`sealevelpressure`) in hPa
  - Cloud Cover (`cloudcover`) in %
  - Season (`season`) – summer, winter, spring, autumn
- GUI built with **Tkinter**
- Color-coded prediction display
- Real-time clock display
- Input validation

---

## Requirements

- Python 3.8+
- Libraries:
```bash
pip install pandas numpy scikit-learn joblib pillow
Pre-trained model file: random_forest_weather_predictor_reduced_features.joblib

Dataset: cairo_merged_with_season.csv
Installation

1.Clone the repository:
git clone <repository_url>
cd WeatherPredict-AI
2.Install dependencies:
pip install pandas numpy scikit-learn joblib pillow

Usage
Training the Model

1.Set dataset path in train_weather_model.py:
file_path = r'D:\Weather api\cairo_merged_with_season.csv'
2.Run the training script:
python train_weather_model.py
This will:

Preprocess features

Train a Random Forest Regressor

Evaluate using Mean Absolute Error (MAE)

Save the pipeline as random_forest_weather_predictor_reduced_features.joblib
Using the GUI

Run the GUI script:
python weather_gui.py
Enter weather parameters in the left panel

Click Predict

See results in the right panel with color-coded temperatures

File Structure
WeatherPredict-AI/
│
├─ train_weather_model.py          # Train and save the model
├─ weather_gui.py                  # Tkinter GUI
├─ cairo_merged_with_season.csv    # Dataset
├─ random_forest_weather_predictor_reduced_features.joblib # Saved model
├─ README.md                       # Documentation

Model Details

Algorithm: Random Forest Regressor

Preprocessing:

Numerical: Median imputation + StandardScaler

Categorical: Most frequent imputation + OneHotEncoder

Features: windspeed, winddir, sealevelpressure, season, cloudcover

Targets: tempmin, tempmax, temp, feelslike
Notes

Ensure season is consistent with training (summer, winter, spring, autumn)

Inputs must be within realistic ranges

The model pipeline already includes preprocessing, so no additional transformations are needed