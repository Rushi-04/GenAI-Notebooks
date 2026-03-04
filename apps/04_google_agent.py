# from dotenv import load_dotenv
# from langchain_community.utilities import GoogleSerperAPIWrapper
# from langchain.agents import create_agent
# from langchain_groq import ChatGroq


# load_dotenv(override=True)

# llm = ChatGroq(model="openai/gpt-oss-120b")
# search = GoogleSerperAPIWrapper()

# agent = create_agent(
#     model=llm,
#     tools=[search.run],
#     system_prompt="You are a agent and can search for any question on google."
# )

# # question = "What was the weather yesterday at Washim, Maharashtra ?"

# while True:
#     query = input("User: ")
#     if query.lower() == "quit" or "bye":
#         print("Goodbye !👋")
#         break

#     response = agent.invoke({"messages": [{"role": "user", "content": query}]})
#     print("AI: ", response["messages"][-1].content)


############################# -- With Memory (without streaming )-- ######################################


# from dotenv import load_dotenv
# from langchain_community.utilities import GoogleSerperAPIWrapper
# from langchain.agents import create_agent
# from langchain_groq import ChatGroq
# from langgraph.checkpoint.memory import MemorySaver
# import streamlit as st


# st.set_page_config(page_title="Flash Chat")
# load_dotenv(override=True)

# llm = ChatGroq(model="openai/gpt-oss-120b")
# search = GoogleSerperAPIWrapper()

# # memory in session
# if "memory" not in st.session_state:
#     st.session_state.memory = MemorySaver()

# # chat_history of whole session
# if "chat_history" not in st.session_state:
#     st.session_state.chat_history = []


# agent = create_agent(
#     model=llm,
#     tools=[search.run],
#     checkpointer=st.session_state.memory,
#     system_prompt="You are a agent and can search for any question on google."
# )

# # question = "What was the weather yesterday at Washim, Maharashtra ?"

# # while True:
# #     query = input("User: ")
# #     if query.lower() == "quit":
# #         print("Goodbye !👋")
# #         break

# #     response = agent.invoke(
# #         {"messages": [{"role": "user", "content": query}]},
# #         {"configurable": {"thread_id": "1"}}
# #         )
# #     print("AI: ", response["messages"][-1].content)

# st.subheader("AnswerFlash: Answer at the speed of light")

# for entry in st.session_state.chat_history:
#     st.chat_message(entry["role"]).markdown(entry["content"])

# query = st.chat_input("Ask Anything...")

# if query:
#     st.chat_message("user").markdown(query)
#     st.session_state.chat_history.append({"role": "user", "content": query})

#     with st.spinner("Thinking..."):
#         response = agent.invoke(
#             {"messages": [{"role": "user", "content": query}]},
#             {"configurable": {"thread_id": "1"}}
#             )
        
#     answer = response["messages"][-1].content
#     st.chat_message("ai").markdown(answer)
#     st.session_state.chat_history.append({"role": "ai", "content": answer})


##################### with streaming ##########################

from dotenv import load_dotenv
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain.agents import create_agent
from langchain_groq import ChatGroq
from langgraph.checkpoint.memory import MemorySaver
import streamlit as st


st.set_page_config(page_title="Flash Chat")
load_dotenv(override=True)

llm = ChatGroq(model="openai/gpt-oss-120b", streaming=True)
search = GoogleSerperAPIWrapper()

# memory in session 
if "memory" not in st.session_state:
    st.session_state.memory = MemorySaver()

# chat_history of whole session
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


agent = create_agent(
    model=llm,
    tools=[search.run],
    checkpointer=st.session_state.memory,
    system_prompt="You are a agent and can search for any question on google."
)

# question = "What was the weather yesterday at Washim, Maharashtra ?"

# while True:
#     query = input("User: ")
#     if query.lower() == "quit":
#         print("Goodbye !👋")
#         break

#     response = agent.invoke(
#         {"messages": [{"role": "user", "content": query}]},
#         {"configurable": {"thread_id": "1"}}
#         )
#     print("AI: ", response["messages"][-1].content)

st.subheader("AnswerFlash: Answer at the speed of light")

for entry in st.session_state.chat_history:
    st.chat_message(entry["role"]).markdown(entry["content"])

query = st.chat_input("Ask Anything...")

if query:
    st.chat_message("user").markdown(query)
    st.session_state.chat_history.append({"role": "user", "content": query})

    with st.spinner("Thinking..."):
        response = agent.stream(
            {"messages": [{"role": "user", "content": query}]},
            {"configurable": {"thread_id": "1"}},
            stream_mode="messages"
            )
        
    # answer = response["messages"][-1].content
    # st.chat_message("ai").markdown(answer)

    ai_container = st.chat_message("ai")
    with ai_container:
        space = st.empty()

        message = ""

        for chunk in response:
            message = message + chunk[0].content
            space.write(message)

    st.session_state.chat_history.append({"role": "ai", "content": message})


    