import google.generativeai as genai
from vertexai.preview.language_models import TextGenerationModel
import vertexai
from google.oauth2 import service_account
import os
from pathlib import Path
from dotenv import load_dotenv

#loading secured keys
load_dotenv("keys.env") 

#Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
SERVICE_ACCOUNT_KEY_PATH = os.getenv("VERTEX_SERVICE_ACCOUNT_PATH") # Raw string for Windows paths# Consider moving to environment variables
VERTEX_MODEL_NAME = "PredictiveMaintenanceAI"  
GEMINI_MODEL_NAME = "gemini-1.5-pro"

#Authentication
def init_vertex_ai():
    try:
        credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_KEY_PATH,
            scopes=["https://www.googleapis.com/auth/cloud-platform"]
        )
        vertexai.init(
            project="smartmineai",
            location="us-central1",
            credentials=credentials
        )
    except Exception as e:
        raise RuntimeError(f"Vertex AI initialization failed: {str(e)}")

# Initialize APIs
init_vertex_ai()
genai.configure(api_key= GEMINI_API_KEY)

# --- Model Functions --- #
def ask_gemini(prompt: str) -> str:
    try:
        model = genai.GenerativeModel(GEMINI_MODEL_NAME)
        response = model.generate_content(prompt)
        if response.text:
            return response.text
        return "[Gemini Error] Empty response"
    except Exception as e:
        return f"[Gemini Error]: {str(e)}"

def ask_vertex(prompt: str) -> str:
    try:
        model = TextGenerationModel.from_pretrained(VERTEX_MODEL_NAME)
        response = model.predict(
            prompt=prompt,
            temperature=0.4,
            max_output_tokens=512
        )
        return response.text
    except Exception as e:
        return f"[Vertex Error]: {str(e)}"

#Unified Chatbot 
def smart_mining_chat(prompt: str) -> str:
    """Route prompts to appropriate AI model."""
    if not prompt.strip():
        return "Please enter a valid question."
    
    prompt_lower = prompt.lower()
    mining_keywords = {
        "predict", "failure", "runtime", "sensor",
        "equipment", "mine", "mining", "machine",
        "health", "maintenance", "diagnostic"
    }
    
    try:
        if any(keyword in prompt_lower for keyword in mining_keywords):
            response = ask_vertex(prompt)
            # Fallback to Gemini if Vertex fails
            if response.startswith("[Vertex Error]"):
                return ask_gemini(prompt)
            return response
        return ask_gemini(prompt)
    except Exception as e:
        return f"System Error: {str(e)}"

# --- For Testing --- #
if __name__ == "__main__":
    while True:
        user_input = input("You: ")
        if user_input.lower() in ("exit", "quit"):
            break
        print("AI:", smart_mining_chat(user_input))