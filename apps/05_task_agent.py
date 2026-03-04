from langchain_groq import ChatGroq
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langgraph.checkpoint.memory import InMemorySaver
from langchain.agents import create_agent
from dotenv import load_dotenv
import streamlit as st

load_dotenv(override=True)
st.set_page_config(page_title="TaskBot")

db = SQLDatabase.from_uri("sqlite:///my_tasks.db")

try:
    db.run("""
        CREATE TABLE IF NOT EXISTS tasks(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        status TEXT CHECK (STATUS IN ('pending', 'in_progress', 'completed')) DEFAULT 'pending',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    print("Table Created Successfully.")
except Exception as e:
    print(f"Error occured while creating a table: {e}")

model = ChatGroq(model="openai/gpt-oss-120b")
toolkit = SQLDatabaseToolkit(db=db, llm=model)
tools = toolkit.get_tools()
memory = InMemorySaver()


system_prompt = """
You are a task management assistant that interacts with a SQL database containing a 'tasks' table.

TASK RULES:
1. Limit SELECT queries to 10 results max with ORDER BY created_at DESC
2. After CREATE/UPDATE/DELETE, confirm with SELECT query
3. If the user requests a list of tasks, present the output in a structured table format to ensure a clean and organized display in a browser.

CRUD OPERATIONS:
    CREATE: INSERT INTO tasks(title, description, status)
    READ: SELECT * FROM tasks WHERE ... LIMIT 10
    UPDATE: UPDATE tasks SET status=? WHERE id=? OR title=?
    DELETE: DELETE FROM tasks WHERE id=? OR titte=?

Table schema: id, title, description, status(pending, in_progress, completed), created_at.
"""

@st.cache_resource
def get_agent():
    agent = create_agent(
        model=model,
        tools=tools,
        checkpointer=memory,
        system_prompt=system_prompt
    )
    return agent

agent = get_agent()

st.subheader("📜TaskBot - Manage your tasks")
st.markdown("Manage your tasks using natural language - powered by LangChain & SQL")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for entry in st.session_state.chat_history:
    st.chat_message(entry["role"]).markdown(entry["content"])

query = st.chat_input("Ask me to manage your tasks...")

if query:
    st.chat_message("user").markdown(query)
    st.session_state.chat_history.append({"role": "user", "content": query})

    with st.spinner("Processing..."):
        response = agent.invoke(
            {"messages": [{"role": "user", "content": query}]},
            {"configurable": {"thread_id": "1"}}
        )
        result = response["messages"][-1].content

    st.chat_message("ai").markdown(result)
    st.session_state.chat_history.append({"role": "ai", "content": result})



# while True:
#     query = input("User: ")
#     if query.lower() == "bye":
#         print("GoodBye !")
#         break

#     response = agent.invoke(
#         {"messages": [{"role": "user", "content": query}]},
#         {"configurable": {"thread_id": "1"}}
#     )
#     result = response["messages"][-1].content
#     print("AI: ", result)