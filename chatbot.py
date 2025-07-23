import gradio as gr
from google.cloud import aiplatform
import google.generativeai as genai

# Initialize Vertex AI and Gemini
PROJECT_ID = "smartmineai"
REGION = "us-central1"
BUCKET = "gs://chintu-smartmining-bucket"
ENDPOINT_ID = "1818465788504309760"

aiplatform.init(
    project=PROJECT_ID, 
    location=REGION, 
    staging_bucket=BUCKET
)
endpoint = aiplatform.Endpoint(
    endpoint_name=ENDPOINT_ID
)

genai.configure(
    api_key="AIzaSyBLx83mpzpexblZVqJKzU7uj6ocZYbrLqg"
)
model = genai.GenerativeModel(
    "gemini-1.5-pro"
)

# Predictive model input structure
def predict_maintenance(sensor_data: dict):
    try:
        prediction = endpoint.predict([sensor_data])
        return prediction.predictions[0]
    except Exception as e:
        return {"error": str(e)}

# Sample sensor data for simulation (in a real app, you'd fetch this live)
def get_latest_sensor_data():
    return {
        "equipment_id": "E005",
        "temperature": 96.4,
        "vibration": 3.78,
        "pressure": 103.6,
        "runtime_hours": 86,
        "fuel_rate": 15.25,
        "last_maintenance": 46
    }

# Main handler for chat
chat_history = []
def chat_with_bot(user_input, chat_history):
    chat_history.append({"role": "user", "parts": [user_input]})

    if any(keyword in user_input.lower() for keyword in ["equipment", "machine", "maintenance", "predict", "sensor", "failure"]):
        sensor_data = get_latest_sensor_data()
        prediction = predict_maintenance(sensor_data)

        if "error" in prediction:
            response = f"❌ Error from predictive model: {prediction['error']}"
        else:
            label = "⚠️ Likely Failure" if prediction >= 0.5 else "✅ No Immediate Risk"
            response = f"Predicted failure probability for equipment {sensor_data['equipment_id']}: {prediction:.2f} → {label}"
    else:
        response = model.generate_content(user_input).text

    chat_history.append({"role": "model", "parts": [response]})
    return response

# Gradio UI
gr.ChatInterface(
    fn=chat_with_bot,
    title="SmartMineAI Chatbot",
    chatbot=gr.Chatbot(height=300),
    textbox=gr.Textbox(placeholder="Type your message...", container=True, scale=7),
    theme="default",
    examples=["Hello!", "What is AI?", "Tell me a joke."],
).launch()
