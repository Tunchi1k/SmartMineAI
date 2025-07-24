from google.cloud import aiplatform

aiplatform.init(
    project = 'smartmineai',
    location= 'us-central1',
    staging_bucket= 'gs://chintu-smartmining-bucket'
)

# Deploying an endpoint for the model so that I run some tests
endpoint = aiplatform.Endpoint(endpoint_name = '1818465788504309760')

#This function Sends sensor data to Vertex AI endpoint and returns prediction.
def predict_maintenance(sensor_data: dict):
    required_fields = ["equipment_id", "failure", "fuel_rate", "last_maintenance", 
                      "pressure", "runtime_hours", "temperature", "vibration"]
    
    # Check for missing fields
    for field in required_fields:
        if field not in sensor_data:
            return {"error": f"Missing field: {field}"}

    try:
        # Convert all values to strings
        string_data = {k: str(v) for k, v in sensor_data.items()}
        prediction = endpoint.predict([string_data])
        return prediction.predictions[0]
    except Exception as e:
        return {"error": str(e)}