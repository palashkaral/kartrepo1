
import streamlit as st
import requests

# Base URL of the Flask backend, reachable via Docker's internal network
# using the container name assigned to the backend container.
BACKEND_URL = "http://backend:7860"

st.title("SuperKart Sales Prediction")

st.write("Enter the product and store details below to predict the total sales revenue.")

# Input fields for product and store data
Product_Weight = st.number_input("Product Weight", min_value=0.0, value=12.66)
Product_Sugar_Content = st.selectbox("Product Sugar Content", ["Low Sugar", "Regular", "No Sugar"])
Product_Allocated_Area = st.number_input("Product Allocated Area", min_value=0.0, max_value=1.0, value=0.05, step=0.01)
Product_MRP = st.number_input("Product MRP", min_value=0.0, value=140.0)
Store_Size = st.selectbox("Store Size", ["High", "Medium", "Small"])
Store_Location_City_Type = st.selectbox("Store Location City Type", ["Tier 1", "Tier 2", "Tier 3"])
Store_Type = st.selectbox("Store Type", ["Supermarket Type1", "Supermarket Type2", "Departmental Store", "Food Mart"])
Product_Id_char = st.selectbox("Product Category Code (from Product Id)", ["FD", "DR", "NC"])
Store_Age_Years = st.number_input("Store Age (Years)", min_value=0, value=20, step=1)
Product_Type_Category = st.selectbox("Product Type Category", ["Perishables", "Non Perishables"])

product_data = {
    "Product_Weight": Product_Weight,
    "Product_Sugar_Content": Product_Sugar_Content,
    "Product_Allocated_Area": Product_Allocated_Area,
    "Product_MRP": Product_MRP,
    "Store_Size": Store_Size,
    "Store_Location_City_Type": Store_Location_City_Type,
    "Store_Type": Store_Type,
    "Product_Id_char": Product_Id_char,
    "Store_Age_Years": Store_Age_Years,
    "Product_Type_Category": Product_Type_Category,
}

if st.button("Predict", type='primary'):
    try:
        response = requests.post(f"{BACKEND_URL}/v1/predict", json=product_data)
        if response.status_code == 200:
            result = response.json()
            predicted_sales = result["Sales"]
            st.success(f"Predicted Product Store Sales Total: {predicted_sales:,.2f}")
        else:
            st.error(f"Error in API request: {response.status_code}")
    except requests.exceptions.RequestException as e:
        st.error(f"Could not reach the backend API: {e}")

st.divider()
st.subheader("Batch Prediction")
uploaded_file = st.file_uploader("Upload a CSV file with the required columns for batch prediction", type=["csv"])
if uploaded_file is not None and st.button("Run Batch Prediction"):
    try:
        files = {"file": uploaded_file.getvalue()}
        response = requests.post(f"{BACKEND_URL}/v1/predictbatch", files=files)
        if response.status_code == 200:
            st.success("Batch prediction complete.")
            st.json(response.json())
        else:
            st.error(f"Error in API request: {response.status_code}")
    except requests.exceptions.RequestException as e:
        st.error(f"Could not reach the backend API: {e}")
