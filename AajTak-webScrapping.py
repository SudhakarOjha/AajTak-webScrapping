import streamlit as st
import requests
from bs4 import BeautifulSoup
from openai import OpenAI

# Set up your Gemini/OpenAI client
client = OpenAI(
    api_key="----API Key------------",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# Scrape Aaj Tak homepage
def get_aajtak_content():
    url = "https://www.aajtak.in/"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        # Extract all text content
        text = soup.get_text(separator=" ", strip=True)
        return text[:5000]  # Limit to first 5000 chars to stay within token limit
    else:
        return "Failed to fetch Aaj Tak website."

# Streamlit UI
st.title("📰 Aaj Tak News Chatbot 🤖")

user_query = st.text_input("Ask anything about what's on Aaj Tak right now:")

if user_query:
    news_content = get_aajtak_content()

    # Prepare messages
    messages = [
        {
            "role": "system",
            "content": (
                f"You are a helpful AI assistant. Here is the current content and explain it well from Aaj Tak News website:\n\n{news_content}\n\n"
                f"Answer the user's question based on this."
            )
        },
        {
            "role": "user",
            "content": user_query
        }
    ]

    # Call Gemini/OpenAI model
    response = client.chat.completions.create(
        model="gemini-2.5-flash",
        messages=messages
    )

    st.subheader("📝 Answer")
    st.write(response.choices[0].message.content)
