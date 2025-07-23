import google.generativeai as genai

# Replace with your API key directly
API_KEY = "AIzaSyBLx83mpzpexblZVqJKzU7uj6ocZYbrLqg"

# Configure the API key
genai.configure(api_key=API_KEY)

# Initialize the model
model = genai.GenerativeModel("models/gemini-1.5-pro")

# Send a test message
response = model.generate_content("Hello, are you working?")

print("Gemini says:", response.text)
