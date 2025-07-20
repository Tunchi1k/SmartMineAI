import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from google.cloud import aiplatform
import joblib 
from sklearn.ensemble import RandomForestClassifier


#Lets initialize our AI platform
aiplatform.init(
  project = 'smartmineai',
  location= 'us-central1'
)

# Training our dataset
'''def train():
    #Load our dataset
    df = pd.read_csv('equipment_data.csv')
    x = df[['temperature', 'vibration', 'pressure', 'runtime_hours', 'fuel_rate', 'last_maintenance']]
    y = df['failure']

    #Train model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(x, y)

    #Save the model
    joblib.dump(model, 'model.joblib')
    print("Model trained and saved successfully.")

if __name__ == "__main__":
    train()'''

model = joblib.load("model.joblib")
sample = pd.DataFrame([[90, 2.5, 120, 200, 14.0, 40]])  # sample input
prediction = model.predict(sample)
print("Predicted failure:", prediction[0])



