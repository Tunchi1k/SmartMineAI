import google.generativeai as genai
from vertexai.preview.language_models import TextGenerationModel
import vertexai
from google.oauth2 import service_account
import os
from pathlib import Path
from dotenv import load_dotenv
import pandas as pd

# --- Configuration --- #
load_dotenv("keys.env")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
SERVICE_ACCOUNT_KEY_PATH = os.getenv("VERTEX_SERVICE_ACCOUNT_PATH")
VERTEX_MODEL_NAME = "PredictiveMaintenanceAI"  
GEMINI_MODEL_NAME = "gemini-1.5-pro"

# Validate environment variables
if not all([GEMINI_API_KEY, SERVICE_ACCOUNT_KEY_PATH]):
    missing = []
    if not GEMINI_API_KEY: missing.append("GEMINI_API_KEY")
    if not SERVICE_ACCOUNT_KEY_PATH: missing.append("VERTEX_SERVICE_ACCOUNT_PATH")
    raise RuntimeError(f"Missing environment variables: {', '.join(missing)}")

# --- Authentication --- #
def init_vertex_ai():
    """Initialize Vertex AI with service account credentials."""
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
genai.configure(api_key=GEMINI_API_KEY)

# --- Model Functions --- #
def ask_gemini(prompt: str, context: str = None) -> str:
    """Query Gemini model with optional context."""
    try:
        model = genai.GenerativeModel(GEMINI_MODEL_NAME)
        full_prompt = f"{context}\n\nQuestion: {prompt}" if context else prompt
        response = model.generate_content(full_prompt)
        return response.text if response.text else "[Gemini Error] Empty response"
    except Exception as e:
        return f"[Gemini Error]: {str(e)}"

def ask_vertex(prompt: str, context: str = None) -> str:
    """Query Vertex AI model with optional context."""
    try:
        model = TextGenerationModel.from_pretrained(VERTEX_MODEL_NAME)
        full_prompt = f"""
        Context Data:
        {context if context else 'No additional context provided'}
        
        Task: {prompt}
        """
        response = model.predict(
            prompt=full_prompt,
            temperature=0.4,
            max_output_tokens=512
        )
        return response.text
    except Exception as e:
        return f"[Vertex Error]: {str(e)}"

# --- Unified Chatbot --- #
def smart_mining_chat(prompt: str, equipment_data: pd.DataFrame = None) -> str:
    """Route prompts to appropriate AI model with optional equipment data."""
    if not prompt.strip():
        return "Please enter a valid question."
    
    # Prepare context if equipment data is provided
    context = None
    if equipment_data is not None:
        context = "Current Equipment Status:\n"
        context += equipment_data.to_markdown(index=False)
    
    prompt_lower = prompt.lower()
    mining_keywords = {
        "predict", "failure", "runtime", "sensor",
        "equipment", "mine", "mining", "machine",
        "health", "maintenance", "diagnostic"
    }
    
    try:
        if any(keyword in prompt_lower for keyword in mining_keywords):
            response = ask_vertex(prompt, context)
            if response.startswith("[Vertex Error]"):
                return ask_gemini(prompt, context)
            return response
        return ask_gemini(prompt, context)
    except Exception as e:
        return f"System Error: {str(e)}"