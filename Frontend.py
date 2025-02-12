

import streamlit as st
import requests

# Replace with your Render backend URL
API_URL = "https://solar-ai-assistant-genai-projects.onrender.com"

st.title("📝 Groq AI Chatbot")

user_input = st.text_input("Ask something:")

if st.button("Submit"):
    response = requests.post(
        f"{API_URL}/ask",
        json={"user_message": user_input}
    )

    if response.status_code == 200:
        data = response.json()
        st.write("💡 Response:", data.get("answer", "No response received."))
    else:
        st.error(f"❌ API Error: {response.status_code}")
        st.json(response.json())
