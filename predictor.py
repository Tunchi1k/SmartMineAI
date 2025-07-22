from google.cloud import aiplatform

aiplatform.init(
    project = 'smartmineai',
    location= 'us-central1',
    staging_bucket= 'gs://chintu-smartmining-bucket'
)

# Deploying an endpoint for the model so that I run some tests
endpoint = aiplatform.Endpoint(endpoint_name = '1818465788504309760')

instances = [
    {
        
        "equipment_id": "EQ123",
        "sensor_1": 0.5,
        "sensor_2": 0.3,
        "sensor_3": 0.2,
        "sensor_4": 0.1,
        "sensor_5": 0.4,
        "sensor_6": 0.6,
        "sensor_7": 0.8,
        "sensor_8": 0.9
    }
]

# Making a prediction
prediction = endpoint.predict(instances = instances)
print("Prediction results:", prediction.predictions)