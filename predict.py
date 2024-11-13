# Import necessary libraries
import streamlit as st
import pandas as pd
import joblib
import numpy as np

# Load the trained model and scaler
model = joblib.load('model.pkl')
scaler = joblib.load('vector.pkl')

# Streamlit app title
st.title("Water Sprinkler Prediction")

# Create input fields for user to enter sensor data
soil_moisture = st.number_input("Soil Moisture (%)", min_value=0.0, max_value=100.0, value=50.0)
temperature = st.number_input("Temperature (°C)", min_value=-30.0, max_value=50.0, value=25.0)
humidity = st.number_input("Humidity (%)", min_value=0.0, max_value=100.0, value=50.0)
light_intensity = st.number_input("Light Intensity (Lux)", min_value=0, value=500)
water_level = st.number_input("Water Level (cm)", min_value=0.0, value=10.0)

# When the "Predict" button is pressed
if st.button("Predict"):
    # Prepare the input data for prediction
    input_data = np.array([[soil_moisture, temperature, humidity, light_intensity, water_level]])
    
    # Scale the input data
    input_scaled = scaler.transform(input_data)
    
    # Make prediction
    prediction = model.predict(input_scaled)
    
    # Display the result
    st.write(f"Predicted Water Sprinkled: {prediction[0]:.2f} liters")

# Run the app with the following command:
# streamlit run your_script_name.py
