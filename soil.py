import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler  # Used instead of TfidfVectorizer in this case
import joblib
data = pd.read_csv('sensor_data.csv')
X = data[['Soil_Moisture', 'Temperature', 'Humidity', 'Light_Intensity', 'Water_Level']]
y = data['Water_Sprinkled']
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)
model = LinearRegression()
model.fit(X_train, y_train)
joblib.dump(scaler, 'vector.pkl')  # Save the scaler
joblib.dump(model, 'model.pkl')    # Save the trained model
print("Model and scaler saved successfully.")
