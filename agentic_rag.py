
import os
from langchain_community.utilities import SQLDatabase
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langgraph.prebuilt import create_react_agent
from langsmith import Client
from langchain_groq import ChatGroq 
from dotenv import load_dotenv
load_dotenv()
# ==============================
# 1️⃣ SET GOOGLE API KEY
# ==============================
# os.environ["GOOGLE_API_KEY"] = "YOUR_GOOGLE_API_KEY"

# ==============================
# 2️⃣ DATABASE CONNECTION
# ==============================
host = "localhost"
port = "3306"
username = "root"
password = "srikar"
database_schema = "project"

mysql_uri = f"mysql+pymysql://{username}:{password}@{host}:{port}/{database_schema}"

db = SQLDatabase.from_uri(mysql_uri)

print(f"Dialect: {db.dialect}")
print(f"Available tables: {db.get_usable_table_names()}")

# ==============================
# 3️⃣ INITIALIZE GEMINI LLM
# ==============================
llm = ChatGroq(
    model_name="llama-3.3-70b-versatile",
    temperature=0.7,
    api_key=os.getenv("GROQ_API_KEY")
)

# ==============================
# 4️⃣ CREATE SQL TOOLKIT
# ==============================
toolkit = SQLDatabaseToolkit(db=db, llm=llm)
tools = toolkit.get_tools()

# ==============================
# 5️⃣ LOAD SQL AGENT SYSTEM PROMPT
# ==============================
client = Client()

prompt_template = client.pull_prompt(
    "langchain-ai/sql-agent-system-prompt"
)

system_prompt = prompt_template.format(
    dialect="mysql",
    top_k=5
)

# ==============================
# 6️⃣ CREATE REACT SQL AGENT
# ==============================
agent_executor = create_react_agent(
    llm,
    tools,
    prompt=system_prompt
)

# ==============================
# 7️⃣ RUN QUERY
# ==============================
# example_query = "How many products are there in the database?"

while True:
    query = input("enter your query: ")
    if query.lower() in ["exit", "quit"]:
        print("Exiting...")
        break

    events = agent_executor.stream(
        {"messages": [("user", query)]},
        stream_mode="values",
    )

    for event in events:
        event["messages"][-1].pretty_print()