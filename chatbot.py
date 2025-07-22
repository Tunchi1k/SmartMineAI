import google.generativeai as genai
import gradio as gr

# Set your API Key
genai.configure(api_key="AIzaSyBLx83mpzpexblZVqJKzU7uj6ocZYbrLqg") 

# Load the Gemini model
model = genai.GenerativeModel("models/gemini-1.5-pro")

# Define the chat function
def chat_with_gemini(message, history):
    try:
        response = model.generate_content(message)
        reply = response.text
        return reply  
    except Exception as e:
        return f"Error: {e}"

# Launch Gradio chat interface
gr.ChatInterface(
    fn=chat_with_gemini,
    title="SmartMining AI Chatbot",
    chatbot=gr.Chatbot(height=400, min_width=600),
    textbox=gr.Textbox(placeholder="Type your message...", container=True, scale=7),
    theme="soft",
    examples=["What causes mining machine failure?", "Give me a weekly prediction of machine status.",],
).launch()
