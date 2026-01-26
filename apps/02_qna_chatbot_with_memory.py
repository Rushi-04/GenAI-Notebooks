# from dotenv import load_dotenv
# from langchain_google_genai import ChatGoogleGenerativeAI
# import streamlit as st

# load_dotenv(override=True)

# llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite")

# memory = []

# prompt = [
#     {"role": "system", "content": "You are a python developer"},
#     {"role": "user", "content": "What is array"}
# ]

# print("-"*10+"Chat with Memory Bot"+"-"*10)

# while True:
#     query = input("User: ")
#     # print("User: "+res.content)

#     if query.lower() in ["end", "exit", "bye"]:
#         print("Goodbye 🫡!")
#         break

#     memory.append({"role": "user", "content": query})
#     res = llm.invoke(memory)
#     memory.append({"role": "ai", "content": res.content})
#     print("AI: "+res.content)



from langchain_google_genai import ChatGoogleGenerativeAI
import streamlit as st
from dotenv import load_dotenv


load_dotenv(override=True)


llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite")

memory = []

# if "messages" not in st.session_state:
#     st.session_state.messages = []

for msg in memory:
    st.chat_message(msg["role"]).markdown(msg["content"])
    


st.title("ChatBuddy - AI with Memory")
st.markdown("Chat with the latest features on the go")


query = st.chat_input("Ask anything...")

if query:
    st.chat_message("user").markdown(query)
    memory.append({"role": "user", "content": query})
    res = llm.invoke(memory)
    memory.append({"role": "ai", "content": res.content})
    st.chat_message("ai").markdown(res.content)



