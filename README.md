# DocuVision AI - Intelligent Document Assistant 🧠

Welcome to **DocuVision AI**, A project dedicated to exploring multimodal Document Intelligence. This application allows users to upload PDF documents, intelligently parse their text and images, and query the entire document naturally using a Large Language Model (LLM).

The core objective of this project was to understand exactly how Retrieval-Augmented Generation (RAG) applications work behind the scenes, specifically going beyond just text and incorporating multi-modal context (images and charts within PDFs). 

When you upload a document, DocuVision AI breaks it apart, embeds both the text and semantic context surrounding the images into vector spaces, and uses an Approximate Nearest Neighbors algorithm to quickly retrieve the most relevant chunks when you ask a question.

## ✨ Key Features

- **Deep PDF Knowledge Extraction:** Upload any standard PDF, and the app reads, embeds, and indexes the content on the fly.
- **Multimodal Context Mapping:** Extracts images from the PDF and semantically associates them with adjacent text. When querying, the LLM not only returns text but can also present relevant visual charts or figures.
- **Local RAG Pipeline:** Leverages HuggingFace models (`multi-qa-mpnet-base-cos-v1`, `gemma-2b-it`) connected locally via Transformers to process data securely.
- **Cross-Lingual Support:** Features built-in structural support for both English and Japanese document structures and respective embedding models.
- **Chat Export & History Management:** A clean sidebar interface allows you to clear conversation history or export your entire chat transcript for future reference.
- 
## 🛠️ Tech Stack
- **Frontend / UI:** [Streamlit](https://streamlit.io/)
- **Embeddings & Vector Search:** `sentence-transformers`, `Annoy (Approximate Nearest Neighbors)`
- **LLM Infrastructure:** `transformers` (PyTorch) running Gemma-2B architecture.
- **Document Processing:** `PyMuPDF (fitz)`, `PyPDF2`, `pikepdf`, `Pillow`

**What I Learned:**
1. **Handling Multi-modal RAG:** Traditional RAG is straightforward with text, but mapping document images to the exact sub-text via cross-referencing XREFs in PyMuPDF is a fascinating challenge. 
2. **Managing State in Streamlit:** Navigating `st.session_state` to keep LLM message history intact across reruns is critical for a smooth user experience.
3. **Environment Security:** Understanding why hardcoding HuggingFace API tokens is a massive security oversight and practicing proper 12-factor app environment configuration.

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/PriyaPandey27/DocuVision-AI
   cd DocuVision AI
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Setup your Environment Variables:
   Set your HuggingFace token in your terminal environment so the models can download:
  
4. Run the Streamlit App:
   ```bash
   streamlit run app.py
   ```

Important Notes:
Remember to install PyTorch with CUDA support on your device as per the official PyTorch installation instructions.
Additional Considerations: For enhanced performance and scalability, consider using a GPU-accelerated environment. Explore advanced question-answering techniques to improve the chatbot's accuracy and versatility.
