

import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
PORT = os.getenv("PORT", "8000")

st.title("🌞 Solar Industry AI Assistant")

user_input = st.text_input("Ask something:")

if st.button("Submit"):
    response = requests.post(
        f"http://localhost:{PORT}/ask",
        json={"user_message": user_input}  # Send as JSON
    )

    if response.status_code == 200:
        data = response.json()
        if "answer" in data:
            st.write("💡 Response:", data["answer"])
        else:
            st.error("⚠️ Unexpected response format.")
            st.json(data)  # Show raw response for debugging
    else:
        st.error(f"❌ API Error: {response.status_code}")
        st.json(response.json())  # Show error details