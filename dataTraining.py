# Name: Lokitha Nilaweera (157736)
# Project: Capstone Project
# Department: Computer Science
# School: Acadia University
# Title: Vehicle Price Predictor - NS
# Supervisor: Dr. Danny Silver
# Program Title: dataTraining.py

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from flask import Flask, jsonify, request
from sklearn.model_selection import KFold
from sklearn.metrics import mean_absolute_error
import numpy as np
from datetime import datetime

app = Flask(__name__)

file_path = 'master_data.csv'
master_data = pd.read_csv(file_path)
master_data['model_year'] = pd.to_numeric(master_data['model_year'], errors='coerce').fillna(0).astype(int)

# Calculate vehicle age from model year
current_year = datetime.now().year
master_data['vehicle_age'] = current_year - master_data['model_year']
master_data['vehicle_age_squared'] = master_data['vehicle_age'] ** 2
master_data['mileage_squared'] = master_data['mileage'] ** 2

features = master_data[['brand', 'model', 'vehicle_age', 'mileage', 'vehicle_age_squared', 'mileage_squared']].dropna()
target = master_data['list_price'][features.index]

# One-hot encode categorical features
features_encoded = pd.get_dummies(features[['brand', 'model']])
features_encoded['vehicle_age'] = features['vehicle_age']
features_encoded['mileage'] = features['mileage']
features_encoded['vehicle_age_squared'] = features['vehicle_age_squared']
features_encoded['mileage_squared'] = features['mileage_squared']

# K-Fold Cross-Validation setup for 10 folds
kf = KFold(n_splits=10, random_state=42, shuffle=True)
fold_performance = []
fold_accuracy = []

# Average vehicle price for the accuracy calculation
average_vehicle_price = target.mean()

# Iterate over each fold
for train_index, test_index in kf.split(features_encoded):
    X_train, X_test = features_encoded.iloc[train_index], features_encoded.iloc[test_index]
    y_train, y_test = target.iloc[train_index], target.iloc[test_index]

    rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
    rf_model.fit(X_train, y_train)

    predictions = rf_model.predict(X_test)
    mae = mean_absolute_error(y_test, predictions)
    fold_performance.append(mae)

    accuracy = mae / average_vehicle_price
    fold_accuracy.append(accuracy)
    print(f"Accuracy for fold {len(fold_performance)}: {accuracy:.2%}")

# Calculate and print average performance and accuracy
average_performance = np.mean(fold_performance)
average_accuracy = np.mean(fold_accuracy)
print(f"Average Mean Absolute Error across 10 folds: {average_performance:.2f}")
print(f"Average Accuracy across 10 folds: {average_accuracy:.2%}")

# Function to predict the price
def predict_price(vehicle_age, brand, model, mileage, trained_model, training_features):
    input_data = pd.DataFrame(columns=training_features.columns)
    input_data.loc[0] = 0
    input_data['vehicle_age'] = vehicle_age
    input_data['mileage'] = mileage
    input_data[f'brand_{brand}'] = 1
    input_data[f'model_{model}'] = 1
    # Predict the price using the trained model
    predicted_price = trained_model.predict(input_data)
    predicted_price_rounded = round(predicted_price[0], 2)
    return predicted_price_rounded

# Flask web server routes (when running locally, change the route of the "static_folder")
app = Flask(__name__, static_url_path='', static_folder='/Users/lokitha/Desktop/vehiclePriceEstimation/website')

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/makes')
def get_makes():
    unique_makes = master_data['brand'].unique().tolist()
    return jsonify(unique_makes)

@app.route('/models/<make>')
def get_models(make):
    unique_models = master_data[master_data['brand'] == make]['model'].unique().tolist()
    return jsonify(unique_models)

@app.route('/years')
def get_years():
    current_year = datetime.now().year
    years = list(range(current_year, current_year - 20, -1))
    return jsonify(years)

@app.route('/options/<brand>/<model>')
def get_options(brand, model):
    filtered_data = master_data[(master_data['brand'] == brand) & 
                                (master_data['model'] == model)]
    
    wheel_configs = filtered_data['wheel_config'].unique().tolist()
    fuel_types = filtered_data['fuel_type'].unique().tolist()
    colors = filtered_data['color'].unique().tolist()

    return jsonify({'wheelConfigurations': wheel_configs, 
                    'fuelTypes': fuel_types, 
                    'colors': colors})

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.form
        model_year = int(data['year'])
        brand = data['make']
        model = data['model']
        mileage = int(data['mileage'])
        condition = data['condition']

        condition_adjustments = {
            'no_issues': 0,
            'accident_major': -0.10,
            'accident_minor': -0.03,
            'rust_major': -0.10,
            'rust_minor': -0.02
        }
        adjustment_factor = condition_adjustments.get(condition, 0)
        prediction = predict_price(model_year, brand, model, mileage, rf_model, X_train)
        adjusted_prediction = prediction * (1 + adjustment_factor)

        matching_cars = master_data[
            (master_data['model_year'] == model_year) &
            (master_data['brand'] == brand) &
            (master_data['model'] == model) &
            (master_data['mileage'] <= mileage + 8000) & 
            (master_data['mileage'] >= mileage - 8000)
        ]

        # Calculate statistics based on the filtered data
        lowest_price = int(matching_cars['list_price'].min()) if not matching_cars.empty else 0
        average_price = float(matching_cars['list_price'].mean()) if not matching_cars.empty else 0
        highest_price = int(matching_cars['list_price'].max()) if not matching_cars.empty else 0

        # Predict the price for the user's input
        prediction = predict_price(model_year, brand, model, mileage, rf_model, X_train)
        prediction = float(prediction)

        # Return the prediction and statistics
        return jsonify({
            'prediction': prediction,
            'averagePrice': average_price,
            'lowestPrice': lowest_price,
            'adjustedPrediction': adjusted_prediction,
            'highestPrice': highest_price
        })
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({'error': str(e)}), 500

# For when running in Heroku
# if __name__ == '__main__':
#     port = int(os.environ.get('PORT', 5000))
#     app.run(host='0.0.0.0', port=port)

# For when running locally
if __name__ == '__main__':
    app.run(debug=True)