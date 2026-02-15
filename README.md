# Text_to_SQL_Agentic_RAG_using_LangGraph

A small interactive demo that turns natural-language questions into SQL (Text → SQL) using a LangGraph + LangChain agentic RAG setup.

- Uses a `react`-style SQL agent built with `langgraph` and `langchain` toolkits
- LLM backend: Groq (`ChatGroq`) — configured via `GROQ_API_KEY`
- Connects to a MySQL database via `SQLDatabase` (SQLAlchemy / PyMySQL)

---

## Features ✅

- Natural-language to SQL with execution against a MySQL database
- Prompt management via LangSmith (pulls a system prompt)
- Streaming agent responses for interactive use

---

## Quickstart 🔧

1. Clone the repo and open the workspace

   ```bash
   git clone <repo-url>
   cd Text_to_SQL_Agentic_RAG_using_LangGraph
   ```

2. Create a Python virtual environment and install dependencies

   ```bash
   python -m venv .venv
   .\.venv\Scripts\activate      # Windows
   python -m pip install -r requirements.txt
   ```

3. Create a `.env` file (example below) and set API keys + DB credentials

   ```env
   GROQ_API_KEY=your_groq_api_key
   # Optional: GOOGLE_API_KEY=your_google_api_key
   DB_HOST=localhost
   DB_PORT=3306
   DB_USER=root
   DB_PASS=your_db_password
   DB_NAME=project
   ```

   Note: `agentic_rag.py` currently hardcodes DB values — using a `.env` and editing the script to read `os.getenv` is recommended (see "Recommended improvements").

4. Run the agent

   ```bash
   python agentic_rag.py
   ```

   Type natural-language queries at the prompt (e.g. "How many products are there in the database?") and type `exit` or `quit` to stop.

---

## How it works (file: `agentic_rag.py`) 🔍

- Connects to MySQL using `SQLDatabase.from_uri`
- Initializes a Groq-based LLM via `ChatGroq`
- Builds a `SQLDatabaseToolkit` to expose DB operations to the agent
- Pulls a system prompt from LangSmith and creates a `react` agent with `create_react_agent`
- Streams agent responses to the console in an interactive loop

---

## Configuration & environment variables ⚙️

- Required: `GROQ_API_KEY` (for Groq LLM access)
- Optional: `GOOGLE_API_KEY` (commented in the script)
- Database connection: either edit the variables in `agentic_rag.py` or set `DB_*` env vars.

Because the repository currently contains hardcoded DB credentials in `agentic_rag.py`, secure your keys and do NOT commit them to source control.

---

## Troubleshooting & tips ⚠️

- Module import errors: run `python -m pip install -r requirements.txt`.
- DB connection fails: ensure MySQL is running, check host/port/user/password, and that the `project` schema exists.
- Missing LLM key: export `GROQ_API_KEY` or add it to `.env`.
- LangSmith prompt pull fails: ensure LangSmith/CLI credentials are configured in your environment (check LangSmith docs).

---

## Recommended improvements (next steps) 💡

- Read DB credentials from environment variables instead of hardcoding.
- Add CLI args or config file to choose model, temperature, or DB.
- Add try/except and input validation for safer runtime behavior.
- Use a least-privileged DB user and enable SSL for production.
- Add unit / integration tests and a `Dockerfile` for reproducible runs.

Example snippet to make DB creds configurable (suggested change):

```python
host = os.getenv("DB_HOST", "localhost")
port = os.getenv("DB_PORT", "3306")
username = os.getenv("DB_USER", "root")
password = os.getenv("DB_PASS", "")
database_schema = os.getenv("DB_NAME", "project")
mysql_uri = f"mysql+pymysql://{username}:{password}@{host}:{port}/{database_schema}"
```

---

## Security & disclaimers 🔐

- Do NOT commit API keys or DB passwords to git.
- This repo is a demo — never point it at production databases without proper safeguards.

---

## Acknowledgements

Built with: `langchain`, `langgraph`, `langchain-groq` (Groq LLM), `langsmith`, and `langchain-community` SQL utilities.

---

## License

No license specified. Add a `LICENSE` file if you plan to publish or share this project publicly.
