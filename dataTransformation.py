import pandas as pd

def get_average_value(year, make, model, odometer):
    # Load the data from the CSV file
    file_path = '/datasheets/kijiji_data_2023-10-03.csv'
    car_df = pd.read_csv(file_path)
    
    # Filter the DataFrame based on user input
    filtered_df = car_df[(car_df['model_year'] == year) & 
                         (car_df['brand'] == make) & 
                         (car_df['model'] == model)]
    
    # Calculate the average value
    if len(filtered_df) > 0:
        average_value = filtered_df['list_price'].mean()
        return average_value
    else:
        return None

# Example usage:
year = 2019
make = 'Honda'
model = 'Pilot'
odometer = 50000

average_value = get_average_value(year, make, model, odometer)

if average_value is not None:
    print(f"The average value of a {year} {make} {model} with {odometer} miles is ${average_value:.2f}")
else:
    print(f"No data available for the specified vehicle.")
