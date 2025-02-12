import os
import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
PORT = int(os.getenv("PORT", 8000))
MODEL_NAME = os.getenv("MODEL_NAME", "llama3-8b-8192")

if not GROQ_API_KEY:
    raise ValueError("❌ GROQ_API_KEY is missing! Add it to your .env file.")

app = FastAPI()

# Define request schema
class QueryRequest(BaseModel):
    user_message: str

@app.get("/")
def home():
    return {"message": "🌞 Solar Industry AI Assistant Use /ask to interact."}

# 🔹 Prompt Engineering Function
def enhance_prompt(user_query: str) -> str:
    prompt_template = f"""
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

    Now, craft a helpful response to the following user query:

   **User:** "{user_query}"
    **AI (Respond in a warm, knowledgeable, and engaging manner):**
    """
    
    
    return prompt_template.strip()

# Function to generate responses via Groq API
def get_chat_response(user_message):
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

    response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=json_data)

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    elif response.status_code == 401:
        return "❌ Error: Unauthorized! Check your Groq API key."
    else:
        return f"❌ Error: {response.status_code} - {response.text}"

@app.post("/ask")
def ask(request: QueryRequest):
    user_message = request.user_message
    if not user_message:
        raise HTTPException(status_code=400, detail="Message cannot be empty.")
    return {"answer": get_chat_response(user_message)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT)