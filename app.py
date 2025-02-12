import os
import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv


# Load environment variables
load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")
PORT = int(os.getenv("PORT", 7860))  # Hugging Face uses port 7860
MODEL_NAME = os.getenv("MODEL_NAME", "deepseek-ai/deepseek-llm-7b-chat")

# Verify Hugging Face token
if not HF_TOKEN:
    raise ValueError("❌ HF_TOKEN is missing! Add it to your Hugging Face Space secrets.")

# Authenticate Hugging Face
login(HF_TOKEN)

app = FastAPI()

# Define request schema
class QueryRequest(BaseModel):
    user_message: str

@app.get("/")
def home():
    return {"message": "🌞 Solar Industry AI Assistant - Use /ask to interact."}

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

# Function to generate responses via Hugging Face API
def get_huggingface_response(user_message):
    enhanced_query = enhance_prompt(user_message)

    headers = {"Authorization": f"Bearer {HF_TOKEN}", "Content-Type": "application/json"}
    json_data = {
        "inputs": enhanced_query,
        "parameters": {"max_length": 500}
    }

    response = requests.post(
        f"https://api-inference.huggingface.co/models/{MODEL_NAME}",
        headers=headers,
        json=json_data
    )

    if response.status_code == 200:
        return response.json()[0]["generated_text"]
    else:
        return f"❌ Error: {response.status_code} - {response.text}"

@app.post("/ask")
def ask(request: QueryRequest):
    user_message = request.user_message
    if not user_message:
        raise HTTPException(status_code=400, detail="Message cannot be empty.")
    
    response = get_huggingface_response(user_message)
    return {"answer": response}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT)



