# Let's start by loading the dataset and taking a look at its structure to understand the data we're working with.

# Load the dataset
file_path = '/mnt/data/master_data.csv'
master_data = pd.read_csv(file_path)

# Display the first few rows of the dataframe to inspect it
master_data.head()

from sklearn.ensemble import RandomForestRegressor

# Initialize the Random Forest Regressor model with 100 trees
rf_model = RandomForestRegressor(n_estimators=100, random_state=42)

# Train the model with the training data
rf_model.fit(X_train, y_train)

# Predict the target variable for the testing set
rf_predictions = rf_model.predict(X_test)

# Calculate the performance of the model
rf_mse = mean_squared_error(y_test, rf_predictions)
rf_r2 = r2_score(y_test, rf_predictions)

(rf_mse, rf_r2)

def predict_price(model_year, brand, model, mileage, trained_model, training_features):
    """
    Predict the price of a vehicle based on the vehicle's year, make, model, and mileage.
    
    Parameters:
    model_year (int): The year of the vehicle.
    brand (str): The make of the vehicle.
    model (str): The model of the vehicle.
    mileage (int): The mileage of the vehicle.
    trained_model (sklearn estimator): The trained machine learning model.
    training_features (pd.DataFrame): The feature dataframe used to train the model, for encoding.
    
    Returns:
    float: The predicted price of the vehicle.
    """
    # Create a dataframe with the input features
    input_data = pd.DataFrame({
        'model_year': [model_year],
        'mileage': [mileage]
    })
    
    # One-hot encode the categorical variables using the training dataset as a template
    input_data = pd.concat([input_data, pd.DataFrame(columns=training_features.columns)], sort=False)
    input_data.fillna(0, inplace=True)
    
    # Set the corresponding brand and model to 1
    if f'brand_{brand}' in input_data.columns:
        input_data[f'brand_{brand}'] = 1
    if f'model_{model}' in input_data.columns:
        input_data[f'model_{model}'] = 1
    
    # Ensure the input is in the same order as the training features
    input_data = input_data.reindex(columns=training_features.columns, fill_value=0)
    
    # Predict the price using the trained model
    predicted_price = trained_model.predict(input_data)
    
    return predicted_price[0]

# Example: Predict the price of a 2015 Toyota Camry with 60000 miles.
predicted_price_example = predict_price(2015, 'Toyota', 'Camry', 60000, rf_model, X_train)
predicted_price_example