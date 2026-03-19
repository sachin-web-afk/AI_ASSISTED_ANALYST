import asyncio
from fastmcp import Client

MCP_URL = "http://127.0.0.1:8004/mcp"


async def main():

    async with Client(MCP_URL) as client:

        while True:
            q = input("\nAsk: ")

            if q.lower() == "exit":
                break

            try:
                response = await client.call_tool(
                    "query",
                    {"question": q}
                )

                # ✅ ONLY EXTRACT CLEAN RESPONSE
                result = response.data

                # ✅ PRINT ONLY HUMAN READABLE TEXT
                print("\n🤖", result.get("analysis", "No response"))

            except Exception as e:
                print("Error:", str(e))


if __name__ == "__main__":
    asyncio.run(main())