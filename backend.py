from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import Config
from databricks_connector import DatabricksConnector
from schema_loader import SchemaLoader
from agent import Agent
from chart_service import generate_chart
from db_tools import DBTools
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

db = DatabricksConnector(
    Config.DATABRICKS_SERVER_HOSTNAME,
    Config.DATABRICKS_HTTP_PATH,
    Config.DATABRICKS_ACCESS_TOKEN
)
tools = DBTools(db)

schema_loader = SchemaLoader(db)
schema = schema_loader.load_schema()

agent = Agent(schema)


@app.post("/query")
async def query(data: dict):

    question = data.get("question")

    if not question or not question.strip():
        return {
            "analysis": "No data found",
            "query": None,
            "data": None,
            "chart": None
        }

    try:

        sql_query = agent.generate_sql(question)

        print("Executing SQL:", sql_query)

        result = tools.select_data(sql_query)

        rows = result.get("rows", [])

        if not rows:
            return {
                "analysis": "No data found",
                "query": sql_query,
                "data": None,
                "chart": None
            }

        MAX_ROWS = 20
        display_rows = rows[:MAX_ROWS]

        current_data = {
            "columns": result.get("columns"),
            "rows": display_rows
        }

        analysis = agent.analyze_result(question, current_data)
        chart = generate_chart(question, current_data)

        return {
            "analysis": analysis["insight"],
            "query": sql_query,
            "data": current_data,
            "chart": chart
        }

    except Exception as e:

        print("ERROR:", str(e))

        return {
            "analysis": "No data found",
            "query": None,
            "data": None,
            "chart": None
        }