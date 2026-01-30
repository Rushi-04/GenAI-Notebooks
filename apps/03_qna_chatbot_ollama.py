from langchain_ollama import ChatOllama
import streamlit as st

llm = ChatOllama(model="gemma3:1b")

st.title("ChatBuddy - AI Assistant at your Service.")
st.markdown("Chatbot created using ollama.")

if "memory" not in st.session_state:
    st.session_state.memory = []

for entry in st.session_state.memory:
    st.chat_message(entry["role"]).markdown(entry["content"])


query = st.chat_input("Ask anything to gemma...")

if query:
    st.chat_message("user").markdown(query)
    st.session_state.memory.append({"role": "user", "content": query})

    with st.spinner("Thinking..."):
        res = llm.invoke(st.session_state.memory)

    st.balloons()

    st.chat_message("ai").markdown(res.content)
    st.session_state.memory.append({"role": "ai", "content": res.content})