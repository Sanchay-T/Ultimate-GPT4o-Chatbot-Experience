# Ultimate GPT-4o Chatbot Experience

Welcome to the Ultimate GPT-4o Chatbot Experience, an advanced platform designed to harness the power of OpenAI's latest GPT-4o model. This repository is perfect for developers, AI enthusiasts, and innovators who want to integrate cutting-edge AI capabilities into their projects.

## About the Project

This project showcases a sophisticated chatbot application using the GPT-4o language model. The application is built with Python and Streamlit, providing an interactive interface for seamless user interactions. The chatbot can handle text and audio inputs, display images, and provide real-time responses.

I am Sanchay Thalnerkar, a data scientist, writer, and content creator. My experience spans various aspects of AI and content creation. For a comprehensive guide on leveraging GPT-4o, please visit my detailed tutorial on lablab: [Unleashing the Power of GPT-4o: A Comprehensive Guide](https://lablab.ai/t/unleashing-the-power-of-gpt-4o-a-comprehensive-guide).


## Features

- **Advanced AI Integration**: Leverage OpenAI's GPT-4o for sophisticated language understanding and response generation.
- **Real-Time Interaction**: Experience immediate responses with real-time streaming capabilities.
- **Multi-Modal Input**: Supports text, audio, and image inputs for a versatile interaction experience.
- **Customizable Settings**: Easily adjust model parameters such as temperature and select different model versions.
- **Interactive Web App**: Built with Streamlit, providing a user-friendly interface for seamless interactions.

## Getting Started

Follow these instructions to set up the project on your local machine for development and testing purposes.

### Prerequisites

- Python 3.7 or higher
- pip and virtualenv

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/<your-username>/Ultimate-GPT4o-Chatbot-Experience.git
   cd Ultimate-GPT4o-Chatbot-Experience
   ```

2. **Set up a virtual environment**

   ```bash
   virtualenv env
   source env/bin/activate  # On macOS and Linux
   .\env\Scripts\activate   # On Windows
   ```

3. **Install the dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**

   Create a `.env` file in the project root directory and add the following:

   ```
   OPENAI_API_KEY=<your_openai_api_key>
   ```

### Running the Application

Execute the following command to run the Streamlit application:

```bash
streamlit run app.py
```

Visit `http://localhost:8501` in your web browser to see the application in action.

## Usage

The application allows you to interact with the GPT-4o model through text and audio inputs. You can also upload images to enhance the interaction experience. Adjust model parameters such as temperature and select different model versions from the sidebar.

## Code Overview

Here is a brief overview of the main code components:

### Streamlit Setup

```python
import streamlit as st
from openai import OpenAI
import dotenv
import os
from PIL import Image
from audio_recorder_streamlit import audio_recorder
import base64
from io import BytesIO

dotenv.load_dotenv()

def stream_llm_response(client, model_params):
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
    buffered = BytesIO()
    image_raw.save(buffered, format=image_raw.format)
    img_byte = buffered.getvalue()
    return base64.b64encode(img_byte).decode("utf-8")

def main():
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
```

## Contributing

We welcome contributions from the community. If you'd like to contribute, please fork the repository and use a feature branch. Pull requests are warmly welcome.

## Acknowledgments

- OpenAI for the GPT-4o model
- Streamlit for enabling rapid application development

## Full Tutorial

For a complete tutorial on how to unleash the power of GPT-4o, visit: [Unleashing the Power of GPT-4o: A Comprehensive Guide](https://lablab.ai/t/unleashing-the-power-of-gpt-4o-a-comprehensive-guide)

---
