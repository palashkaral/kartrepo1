
# Import necessary libraries
import numpy as np
import joblib  # For loading the serialized model
import pandas as pd  # For data manipulation
from flask import Flask, request, jsonify  # For creating the Flask API

# Initialize the Flask application
superkart_api = Flask("SuperKart Sales Prediction API")

# Load the trained machine learning model (pipeline includes preprocessing + regressor)
model = joblib.load("superkart_sales_prediction_model_v1_0.joblib")

# Define a route for the home page (GET request)
@superkart_api.get('/')
def home():
    """
    Handles GET requests to the root URL ('/') of the API.
    Returns a simple welcome message.
    """
    return "Welcome to the SuperKart Sales Prediction API!"


# Define an endpoint for single (online) prediction
@superkart_api.post('/v1/predict')
def predict_sales():
    """
    Handles POST requests to '/v1/predict'.
    Expects a JSON payload with the product/store features and
    returns the predicted Product_Store_Sales_Total.
    """
    # Get JSON data from the request
    data = request.get_json()

    # Extract relevant features from the input data (order does not matter -
    # the preprocessing pipeline selects columns by name)
    sample = {
        'Product_Weight': data['Product_Weight'],
        'Product_Sugar_Content': data['Product_Sugar_Content'],
        'Product_Allocated_Area': data['Product_Allocated_Area'],
        'Product_MRP': data['Product_MRP'],
        'Store_Size': data['Store_Size'],
        'Store_Location_City_Type': data['Store_Location_City_Type'],
        'Store_Type': data['Store_Type'],
        'Product_Id_char': data['Product_Id_char'],
        'Store_Age_Years': data['Store_Age_Years'],
        'Product_Type_Category': data['Product_Type_Category'],
    }

    # Convert the extracted data into a single-row DataFrame
    input_data = pd.DataFrame([sample])

    # Make a sales prediction using the trained model pipeline
    prediction = model.predict(input_data).tolist()[0]

    # Return the prediction as a JSON response
    return jsonify({'Sales': prediction})


# Define an endpoint for batch prediction (CSV upload)
@superkart_api.post('/v1/predictbatch')
def predict_sales_batch():
    """
    Handles POST requests to '/v1/predictbatch'.
    Expects a CSV file (field name 'file') containing rows with the same
    feature columns as the single-prediction endpoint, and returns a JSON
    object mapping each row index to its predicted sales value.
    """
    file = request.files['file']
    batch_data = pd.read_csv(file)

    required_columns = [
        'Product_Weight', 'Product_Sugar_Content', 'Product_Allocated_Area',
        'Product_MRP', 'Store_Size', 'Store_Location_City_Type', 'Store_Type',
        'Product_Id_char', 'Store_Age_Years', 'Product_Type_Category',
    ]
    batch_input = batch_data[required_columns]

    predictions = model.predict(batch_input).tolist()

    results = {str(idx): pred for idx, pred in enumerate(predictions)}
    return jsonify(results)


# Run the Flask app in debug mode (used only for local/manual testing;
# the Docker container instead runs this via gunicorn - see Dockerfile below)
if __name__ == '__main__':
    superkart_api.run(debug=True)
