import pandas as pd

def get_average_value():
    year = input("Enter the year of the vehicle: ")
    make = input("Enter the make of the vehicle: ")
    model = input("Enter the model of the vehicle: ")
    odometer = int(input("Enter the odometer reading of the vehicle: "))

    file_path = '/Users/lokitha/Desktop/Final Project/dataExtractionProgram/datasheets/kijiji_data_2023-10-03.csv'  # Adjust the file path as needed

    try:
        car_df = pd.read_csv(file_path)
        filtered_df = car_df[(car_df['model_year'] == int(year)) & 
                             (car_df['brand'] == make) & 
                             (car_df['model'] == model)]
        
        if not filtered_df.empty:
            avg_price = filtered_df['list_price'].mean()
            print(f"The average price for a {year} {make} {model} with {odometer} miles is: ${avg_price:.2f}")
        else:
            print(f"No data found for {year} {make} {model}.")

    except FileNotFoundError:
        print(f"File '{file_path}' not found.")

get_average_value()