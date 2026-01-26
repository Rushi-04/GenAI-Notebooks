from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
import streamlit as st
import os
# from streamlit_autorefresh import st_autorefresh

load_dotenv(override=True)
# print(os.getenv("GEMINI_API_KEY"))

# count = st_autorefresh(interval=2000, limit=100, key="fizzbuzzcounter")
# st.write(f"Count: {count}")

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite")


# while True:
#     query = input("User: ")
    
#     if query.lower() in ["lower", "quit", "bye"]:
#         print("Good Bye !")
#         break

#     res = llm.invoke(query)
#     print("AI: "+res.content)

st.title("ChatBuddy - AI Chatbot Assistant")
st.markdown("My QnA Chatbot using Langchain and google gemini")

query = st.chat_input("Ask anything ...")


if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    role = msg["role"]
    content =  msg["content"]
    st.chat_message(role).markdown(content)


if query:
    st.chat_message("user").markdown(query)
    st.session_state.messages.append({"role": "user", "content": query})
    res = llm.invoke(st.session_state.messages)
    st.chat_message("ai").markdown(res.content)
    st.session_state.messages.append({"role": "ai", "content": res.content})