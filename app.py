import streamlit as st
from openai import OpenAI
import dotenv
import os
from PIL import Image
from audio_recorder_streamlit import audio_recorder
import base64
from io import BytesIO

# Load environment variables from a .env file
dotenv.load_dotenv()

def stream_llm_response(client, model_params):
    """Function to stream the response from the language model in real-time."""
    response_message = ""
    for chunk in client.chat.completions.create(
        model=model_params["model"] if "model" in model_params else "gpt-4o-2024-05-13",
        messages=st.session_state.messages,
        temperature=(model_params["temperature"] if "temperature" in model_params else 0.3),
        max_tokens=4096,
        stream=True,
    ):
        response_message += chunk.choices[0].delta.content if chunk.choices[0].delta.content else ""
        yield chunk.choices[0].delta.content if chunk.choices[0].delta.content else ""
    
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": [{"type": "text", "text": response_message}],
        }
    )

def get_image_base64(image_raw):
    """Convert an image file to a base64-encoded string."""
    buffered = BytesIO()
    image_raw.save(buffered, format=image_raw.format)
    img_byte = buffered.getvalue()
    return base64.b64encode(img_byte).decode("utf-8")

def main():
    """Main function to configure and run the Streamlit app."""
    st.set_page_config(
        page_title="GPT-4o Chatbot Experience",
        page_icon="🤖",
        layout="centered",
        initial_sidebar_state="expanded",
    )

    st.markdown(
        """
        <div style="text-align: center; padding: 10px;">
            <h1 style="color: #4CAF50;">🌟 The Ultimate GPT-4o Chatbot Experience 🌟</h1>
            <p style="font-size: 20px; color: #888;">Unleash the power of AI with our advanced assistant!</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.sidebar:
        default_openai_api_key = os.getenv("OPENAI_API_KEY", "")
        openai_api_key = st.text_input(
            "Paste your OpenAI API Key (https://platform.openai.com/)",
            value=default_openai_api_key,
            type="password",
        )

    if openai_api_key == "" or openai_api_key is None or "sk-" not in openai_api_key:
        st.warning("⬅️ Please introduce your OpenAI API Key (make sure to have funds) to continue...")
    else:
        client = OpenAI(api_key=openai_api_key)
        if "messages" not in st.session_state:
            st.session_state.messages = []

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                for content in message["content"]:
                    if content["type"] == "text":
                        st.write(content["text"])
                    elif content["type"] == "image_url":
                        st.image(content["image_url"]["url"])

        with st.sidebar:
            model = st.selectbox(
                "Select a model:",
                ["gpt-4o-2024-05-13", "gpt-4-turbo"],
                index=0,
            )
            model_temp = st.slider("Temperature", min_value=0.0, max_value=2.0, value=0.3, step=0.1)
            model_params = {
                "model": model,
                "temperature": model_temp,
            }

        if st.button("🗑️ Reset conversation"):
            st.session_state.messages = []

        prompt = st.text_input("Hi! I am the latest omnimodel from OpenAI, ask me anything!")
        if prompt:
            st.session_state.messages.append(
                {
                    "role": "user",
                    "content": [{"type": "text", "text": prompt}],
                }
            )
            with st.spinner('Waiting for response...'):
                for response in stream_llm_response(client, model_params):
                    st.write(response)

if __name__ == "__main__":
    main()
