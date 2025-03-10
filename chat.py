import streamlit as st
from llama_index.indices.managed.llama_cloud import LlamaCloudIndex
from llama_index.core.chat_engine import CondensePlusContextChatEngine

# Streamlit UI
st.title("ASF Chatbot")
st.write("Cu ce informație vă pot ajuta?")

# Load LlamaCloudIndex
index = LlamaCloudIndex(
    name="wee-slug-2025-03-10",
    project_name="ASF_CHATBOT",
    organization_id=st.secrets["api"]["organization_id"],
    api_key=st.secrets["api"]["llama_cloud_api_key"]
)

# Initialize chat engine
chat_engine = CondensePlusContextChatEngine.from_defaults(
    index.as_retriever(),
    chat_mode="condense_plus_context",
    context_prompt=(
        "You are a chatbot, able to have normal interactions, as well as talk "
        "about financial reports. Here are the relevant documents for context:\n"
        "{context_str}\n"
        "Instruction: Based on the above documents, provide a detailed answer for the user question below."
    ),
)

# User input
query = st.text_input("Întrebare:")

if query:
    # Display loading spinner
    with st.spinner("Caut informația solicitată..."):

        # Stream the response
        response = chat_engine.stream_chat(query)

        # Display response dynamically
        st.subheader("Răspuns:")
        response_text = ""
        response_container = st.empty()  # Placeholder for dynamic updates

        for token in response.response_gen:
            response_text += token
            response_container.write(response_text)  # Update progressively
