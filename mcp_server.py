from fastapi import FastAPI
from pydantic import BaseModel, Field
import os

from agent import Agent
from chart_service import generate_chart
from db_tools import DBTools
from databricks_connector import DatabricksConnector
from schema_loader import SchemaLoader
from config import Config
from fastmcp import FastMCP

mcp = FastMCP(name = "Databricks mcp server")


class QueryRequest(BaseModel):
    question: str = Field(example="show top 5 universities")


print("🚀 Connecting to Databricks...")

db = DatabricksConnector(
    Config.DATABRICKS_SERVER_HOSTNAME,
    Config.DATABRICKS_HTTP_PATH,
    Config.DATABRICKS_ACCESS_TOKEN
)

tools = DBTools(db)

schema = SchemaLoader(db).load_schema()
agent = Agent(schema)

print("✅ MCP Server Ready")


@mcp.tool()
def query(question:str):


    try:

        sql = agent.generate_sql(question)

        print("Executing SQL:", sql)

        result = tools.select_data(sql)

        rows = result.get("rows", [])

        if not rows:
            return {
                "analysis": "No data found",
                "data": None,
                "chart": None
            }

        data_clean = {
            "columns": result["columns"],
            "rows": rows[:20]
        }

        analysis = agent.analyze_result(question, data_clean)
        chart = generate_chart(question, data_clean)

        return {
            "analysis": analysis["insight"],
            "data": data_clean,
            "chart": chart
        }

    except Exception as e:

        print("ERROR:", str(e))

        return {
            "analysis": "No data found",
            "data": None,
            "chart": None
        }




if __name__ == "__main__":
    mcp.run(
        transport="streamable-http",
        host="0.0.0.0", 
        port=int(os.environ.get("PORT", 10000)),  \
        path="/mcp"
    )
    