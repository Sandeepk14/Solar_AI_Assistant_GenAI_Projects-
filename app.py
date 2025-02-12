import os
import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Load API key & model
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME", "llama3-8b-8192")
PORT = int(os.getenv("PORT", 10000))  # Render uses dynamic ports

# Validate API Key
if not GROQ_API_KEY:
    raise ValueError("❌ GROQ_API_KEY is missing! Add it to your Render environment variables.")

app = FastAPI()

# Define request schema
class QueryRequest(BaseModel):
    user_message: str

@app.get("/")
def home():
    return {"message": "🌞 Solar Industry AI Assistant - Use /ask to interact."}

# 🔹 Enhanced Prompt Engineering Function
def enhance_prompt(user_query: str) -> str:
    return f"""
    You are a friendly and knowledgeable AI assistant specializing in solar energy. Your responses should be:

    - **Engaging:** Greet users warmly and make the conversation feel natural.
    - **Technical yet Simple:** Provide well-researched, expert answers in easy-to-understand terms.
    - **Practical:** Offer **real-world examples** and actionable insights.
    - **Conversational:** Respond in a **helpful and friendly tone**.

    **Example Queries:**
    1️⃣ **User:** "What are the benefits of solar panels?"
       **AI:** ✅ "Solar panels offer cost savings, environmental benefits, and energy independence."

    2️⃣ **User:** "How do I install solar panels?"
       **AI:** ✅ "Installation involves site assessment, panel mounting, electrical wiring, and grid connection."

    Now, answer the following query:
    **User:** "{user_query}"
    **AI:**
    """.strip()

# 🔹 Function to Generate Responses via Groq API
def get_chat_response(user_message: str):
    enhanced_query = enhance_prompt(user_message)  # Apply prompt engineering

    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
    json_data = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": "You are a helpful AI assistant."},
            {"role": "user", "content": enhanced_query}
        ],
        "temperature": 0.7
    }

    try:
        response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=json_data)
        response.raise_for_status()  # Raise an error for non-200 responses
        return response.json()["choices"][0]["message"]["content"]
    except requests.exceptions.RequestException as e:
        return f"❌ API Request Error: {str(e)}"

@app.post("/ask")
def ask(request: QueryRequest):
    if not request.user_message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty.")
    
    return {"answer": get_chat_response(request.user_message)}

# Run FastAPI Server for Render
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT)
