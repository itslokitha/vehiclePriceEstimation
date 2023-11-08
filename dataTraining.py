import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from flask import Flask, jsonify, request

# Load and preprocess the dataset
file_path = 'master_data.csv'  # Change to the correct path or a URL if needed
master_data = pd.read_csv(file_path)

# Assuming preprocessing steps here...
# (Make sure to include the preprocessing steps before splitting the data)

# Split the data into training and testing sets
X = master_data.drop('list_price', axis=1)
y = master_data['list_price']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize and train the Random Forest Regressor model
rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

# Function to predict the price
def predict_price(model_year, brand, model, mileage, trained_model, training_features):
    # Preprocessing and prediction logic...
    # (Remember to indent all lines of code within this function)

# Flask web server
    app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    prediction = predict_price(
        data['year'], data['make'], data['model'], data['mileage'],
        rf_model, X_train
    )
    return jsonify({'prediction': prediction})

if __name__ == '__main__':
    app.run(debug=True)
