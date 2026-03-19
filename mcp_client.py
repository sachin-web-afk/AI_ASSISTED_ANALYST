import requests

MCP_URL = "http://localhost:8004"

class MCPClient:

    def ask(self, question):
        res = requests.post(
            f"{MCP_URL}/query",
            json={"question": question}
        )
        return res.json()