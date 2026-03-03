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


############################# -- With Memory -- ######################################


from dotenv import load_dotenv
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain.agents import create_agent
from langchain_groq import ChatGroq
from langgraph.checkpoint.memory import MemorySaver


load_dotenv(override=True)

llm = ChatGroq(model="openai/gpt-oss-120b")
search = GoogleSerperAPIWrapper()
memory = MemorySaver()

agent = create_agent(
    model=llm,
    tools=[search.run],
    checkpointer=memory,
    system_prompt="You are a agent and can search for any question on google."
)

# question = "What was the weather yesterday at Washim, Maharashtra ?"

while True:
    query = input("User: ")
    if query.lower() == "quit":
        print("Goodbye !👋")
        break

    response = agent.invoke(
        {"messages": [{"role": "user", "content": query}]},
        {"configurable": {"thread_id": "1"}}
        )
    print("AI: ", response["messages"][-1].content)


