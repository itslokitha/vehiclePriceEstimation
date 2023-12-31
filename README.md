# Vehicle Price Estimation System

## Overview

This repository contains a system that estimates and predicts the current and past market price (minimum, mean, maximum values) of used personal-use vehicles. The system targets sellers who want to place selling prices on their vehicles. It accomplishes this by utilizing a browser-based website, Kijiji, and a set of programs for data extraction, transformation, and scheduling.

## Programs

### 1. Extraction Program
- **Functionality (F1):** This program extracts vehicle data from the Kijiji website, collecting attributes like make, model, year, list price, color, condition, body type, wheel configuration, transmission, fuel type, mileage, VIN number, image link, and seller’s address. The data is saved in a separate CSV file for each day.

### 2. Transformation Program
- **Functionality (F2):** This program processes the data extracted by the Extraction program. It identifies duplicates for each vehicle and creates a master CSV file containing only the original data. The master file is free of duplicates.

### 3. Scheduler Program
- **Functionality (F3):** This program schedules the Extraction and Transformation programs to run daily at specific times. It ensures the continuous and automated execution of these tasks.

## User Interface

### 1. Price Estimation Interface (UF1)
- The system displays estimated values for the current and past market prices of vehicles for the last 2 years and the current year.
- It provides minimum, mean, and maximum values, presented in a gauge-like format.
- Graphical representations show past values.

### 2. Data Generation Interface (UF2)
- Users can select their location from five regions in Nova Scotia (e.g., Valley, Halifax).
- They can choose the current month or quarter as the date.
- Users input vehicle details like make, model, year, and mileage via the keyboard.

## Repository Structure

- `extraction/`: Contains the Extraction program files.
- `dataTransformation/`: Contains the Transformation program files.
- `schedule/`: Contains the Scheduler program files.
- `datasheets/`: Stores the CSV files generated by the Extraction program.
- `master_data.csv/`: Contains the master CSV file created by the Transformation program.

## Usage

1. Clone the repository.
2. Run the Scheduler program to automate the Extraction and Transformation tasks.
3. Use the Price Estimation Interface to get current and past market price estimates.
4. Utilize the Data Generation Interface to input vehicle details for estimation.

## Contributing

- Fork the repository.
- Create a new branch for your changes.
- Make your contributions.
- Create a pull request.

---

For any inquiries, please contact Lokitha Nilaweera (mailto:anuja.lokitha@outlook.com).
