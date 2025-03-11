import streamlit as st
from llama_index.indices.managed.llama_cloud import LlamaCloudIndex
from llama_index.core.chat_engine import CondensePlusContextChatEngine
from llama_index.core.memory import ChatMemoryBuffer

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
memory = ChatMemoryBuffer.from_defaults(token_limit=10000)
chat_engine = CondensePlusContextChatEngine.from_defaults(
    index.as_retriever(),
    chat_mode="condense_plus_context",
    memory = memory,
    context_prompt=(
        "Ești un chatbot specializat în legislație și reglementări din domeniul financiar, "
        "emis de Autoritatea de Supraveghere Financiară (ASF) din România. "
        "Poți oferi răspunsuri clare și detaliate bazate pe documentele oficiale disponibile.\n\n"
        "Documentele relevante pentru acest context sunt:\n"
        "{context_str}\n\n"
        "Instrucțiuni: Pe baza documentelor de mai sus, oferă un răspuns detaliat și precis "
        "la întrebarea utilizatorului. Dacă informațiile nu sunt disponibile, indică acest lucru clar."
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
