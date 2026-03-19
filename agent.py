import json
import re
import requests
from langchain_groq import ChatGroq
from config import Config

PROMPT_URL = "http://localhost:8002"


class Agent:

    def __init__(self, schema):
        self.schema = schema
        self.table = list(schema.keys())[0]

        self.llm = ChatGroq(
            api_key=Config.GROQ_API_KEY,
            model="llama-3.1-8b-instant",
            temperature=0.1
        )

    def get_prompt(self, endpoint):
        res = requests.get(f"{PROMPT_URL}{endpoint}")
        return res.json()["prompt"]

    def clean_sql(self, text):

        if not text:
            return None

        text = text.replace("```sql", "").replace("```", "").strip()

        if "{" in text and "}" in text:
            try:
                start = text.find("{")
                end = text.rfind("}") + 1
                data = json.loads(text[start:end])
                return data.get("query")
            except:
                pass

        return text.strip()

    def fix_sql(self, query):

        if not query:
            return None

        # remove TOP
        query = re.sub(r"TOP\s+\d+", "", query, flags=re.IGNORECASE)

        # remove duplicate LIMIT
        query = re.sub(
            r"(LIMIT\s+\d+)\s+LIMIT\s+\d+",
            r"\1",
            query,
            flags=re.IGNORECASE
        )

        # add LIMIT if missing
        if "limit" not in query.lower():
            query = query.strip().rstrip(";") + " LIMIT 5"

        return query

    def fix_name_matching(self, query):

        return re.sub(
            r"University_Name\s*=\s*'(.*?)'",
            r"University_Name LIKE '%\1%'",
            query,
            flags=re.IGNORECASE
        )

    def fix_location_matching(self, query):

        mapping = {
            "california": "CA",
            "new york": "NY",
            "texas": "TX"
        }

        for k, v in mapping.items():
            query = re.sub(
                rf"State\s*=\s*'{k}'",
                f"State = '{v}'",
                query,
                flags=re.IGNORECASE
            )

        return query

    def generate_sql(self, question):

        template = self.get_prompt("/prompts/sql")

        prompt = template.format(
            table=self.table,
            schema=self.schema,
            question=question
        )

        response = self.llm.invoke(prompt)

        raw = response.content
        print("LLM RAW >>>", raw)

        query = self.clean_sql(raw)
        query = self.fix_sql(query)
        query = self.fix_name_matching(query)
        query = self.fix_location_matching(query)

        if not query:
            raise Exception("No data found")

        return query.strip()

    def analyze_result(self, question, data):

        template = self.get_prompt("/prompts/analysis")

        prompt = template.format(
            question=question,
            data=data.get("rows", [])[:5]
        )

        response = self.llm.invoke(prompt)

        return {
            "insight": response.content.strip()
        }