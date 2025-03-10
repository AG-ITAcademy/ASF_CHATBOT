import streamlit as st
from llama_index.indices.managed.llama_cloud import LlamaCloudIndex

# Streamlit UI
st.title("ASF Chatbot")
st.write("Cu ce informatie va pot ajuta?")

# User input
query = st.text_input("Intrebare:")

# Only run if the user enters a query
if query:
    # Load LlamaCloudIndex
    index = LlamaCloudIndex(
        name="wee-slug-2025-03-10",
        project_name="ASF_CHATBOT",
        organization_id=st.secrets["api"]["organization_id"],
        api_key=st.secrets["api"]["llama_cloud_api_key"]
    )

    # Get response
    with st.spinner("Caut informatia solicitata..."):
        response = index.as_query_engine().query(query)

    # Display answer
    st.subheader("Raspuns:")
    st.write(response)
