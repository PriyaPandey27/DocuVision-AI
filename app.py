import base64
import streamlit as st
import random
import time
from streamlit_authenticator import Authenticate
import yaml
from yaml.loader import SafeLoader
from pdf_text_processor import TextGen
import os
from pdf_image_processor import Image_Gen
from PIL import Image
import pandas as pd
import uuid

st.set_page_config(page_title="InsightAI", page_icon="🧠", layout="wide", initial_sidebar_state="expanded")

# Function to display PDF from bytes

@st.cache_resource
def loading_llm():
    return TextGen(), Image_Gen()

text_model, image_model = loading_llm()

def display_pdf_from_bytes(pdf_data):
    pdf_data = base64.b64encode(pdf_data).decode('utf-8')
    pdf_display = (
        f'<embed src="data:application/pdf;base64,{pdf_data}" '
        'width="500" height="800" type="application/pdf"></embed>'
    )
    st.sidebar.markdown(pdf_display, unsafe_allow_html=True)

def toggle_related_images():
    if st.session_state.show_related_images:
        st.session_state.show_related_images = False
        return "View related images"
    else:
        st.session_state.show_related_images = True
        return "Hide images"

# Function to display related images in a carousel layout
def display_related_images():
    image_paths = ["image1.jpg", "image2.jpg"]  # Update these paths to the locations of your images
    for image_path in image_paths:
        with open(image_path, "rb") as f:
            image_bytes = f.read()
        st.sidebar.image(image_bytes, caption="Related Image", use_column_width=True)

# Streamed response emulator
def response_generator():
    response = random.choice(
        [
            "Hello there! How can I assist you today?",
            "Hi, human! Is there anything I can help you with?",
            "Do you need help?",
        ]
    )
    for word in response.split():
        yield word + " "
        time.sleep(0.05)

# Main function
def main():

    with open('config.yaml') as file:
        config = yaml.load(file, Loader=SafeLoader)

    authenticator = Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days'],
        config['preauthorized']
    )

    _, st.session_state.authentication_status, _ = authenticator.login(location='main')


    if st.session_state.authentication_status:
        # Check if a unique ID already exists in the session state
        if 'session_id' not in st.session_state:
            # Generate a new unique ID
            st.session_state.session_id = str(uuid.uuid4())
            os.makedirs(os.path.join(text_model.datafolder, st.session_state.session_id), exist_ok=True)
        
        if 'str2' not in st.session_state:        
            st.session_state.str2=[0]
        
        st.sidebar.markdown("# InsightAI")
        st.sidebar.image("your_logo.png", width=250)
        st.sidebar.title("PDF Viewer")
        st.title("InsightAI - Intelligent Document Assistant 🧠")

        # Language selection dropdown
        selected_language = st.sidebar.selectbox("Select Language", options=["English", "Japanese"], index=0)
        
        st.session_state.selected_language = selected_language

        st.markdown("Upload a document using the sidebar to begin extracting insights, querying facts, and viewing associated images!")
        st.markdown("---")
        # if "show_related_images" not in st.session_state:
        #     st.session_state.show_related_images = False

        # PDF uploader
        st.session_state.uploaded = st.sidebar.file_uploader(label="Please browse for a PDF file", type="pdf")
        
        # Tools in sidebar
        st.sidebar.markdown("---")
        st.sidebar.markdown("### Chat Tools")
        if st.sidebar.button("Clear Chat 🗑️"):
            st.session_state.messages = [{"role": "assistant", "content": "Session cleared. How can I help you with this document?"}]
        
        # Initialize chat history early so we can export it
        if "messages" not in st.session_state:
            st.session_state.messages = [{"role": "assistant", "content": "Hello! I am InsightAI. Please upload a PDF to get started."}]
            
        if len(st.session_state.messages) > 1:
            chat_export = "\\n".join([f"{msg['role'].title()}: {msg['content']}" if isinstance(msg['content'], str) else f"{msg['role'].title()}: [Image]" for msg in st.session_state.messages])
            st.sidebar.download_button(
                label="Export Chat 📥",
                data=chat_export,
                file_name="insight_ai_chat.txt",
                mime="text/plain"
            )

        authenticator.logout('Logout', 'sidebar')

        if st.session_state.uploaded is not None:
            
            # Display PDF directly from bytes
            # Process the PDF using TextGen class
            str1=[st.session_state.uploaded]
            
            if str1[0]!=st.session_state.str2[0]:
                st.session_state.paragraphs, st.session_state.vector_dim = text_model.process_pdf(st.session_state.uploaded, st.session_state.selected_language, st.session_state.session_id)
                
                try:
                    st.session_state.paragraphs_image, st.session_state.vector_dim_image = image_model.process_pdf(os.path.join("data", st.session_state.session_id, st.session_state.uploaded.name), st.session_state.session_id, st.session_state.uploaded.name, st.session_state.selected_language)
                except:
                    pass

                # Display PDF on the sidebar
                display_pdf_from_bytes(st.session_state.uploaded.read())
                st.session_state.str2[0]=str1[0]


        # Clickable element to view or hide related images
        # toggle_button_label = toggle_related_images()
        # if st.sidebar.button(toggle_button_label):
        #     toggle_related_images()

        # # Display or hide related images based on toggle state
        # if st.session_state.show_related_images:
        #     display_related_images()

        # authenticator.logout('Logout', 'sidebar')

        # Display chat messages from history on app rerun
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                if isinstance(message["content"], str):
                    st.markdown(message["content"])
                else:
                    try:
                        st.image(message["content"])
                    except:
                        pass

        # Accept user input
        if prompt := st.chat_input("Ask a question about the document..."):
            if st.session_state.uploaded is None:
                st.warning("⚠️ Please upload a PDF from the sidebar before chatting!")
            else:
                # Add user message to chat history
                st.session_state.messages.append({"role": "user", "content": prompt})
            
            # Display user message in chat message container
            with st.chat_message("user"):
                st.markdown(prompt)

            st.session_state.response = {}
            
            # Process the query using TextGen class
            
            st.session_state.response['text'] = text_model.process_query(prompt, st.session_state.selected_language, st.session_state.paragraphs, st.session_state.session_id, st.session_state.uploaded.name, st.session_state.vector_dim)
            
            try:
                st.session_state.response['image'] = image_model.query(prompt, os.path.join("data", st.session_state.session_id, st.session_state.uploaded.name), st.session_state.uploaded.name, st.session_state.selected_language, st.session_state.session_id, st.session_state.vector_dim_image, st.session_state.paragraphs_image)
            except:
                pass
            
            # Display assistant response in chat message container
            with st.chat_message("assistant"):
                st.markdown(st.session_state.response['text'].decode('utf-8'))
                st.session_state.messages.append({"role":"assistant","content":st.session_state.response['text'].decode('utf-8')})
            
            try:
                for image_path in st.session_state.response['image']:    
                    st.image(image_path)
                    st.session_state.messages.append({"role":"assistant","content":Image.open(image_path)})
            except:
                pass
            
if __name__ == "__main__":
    main()
