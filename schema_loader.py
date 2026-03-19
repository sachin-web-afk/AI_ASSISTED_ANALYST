class SchemaLoader:

    def __init__(self, db):

        self.db = db
        self.schema = None

    def load_schema(self):

        tables_query = "SHOW TABLES"

        tables_result = self.db.run_query(tables_query)

        tables = [row[1] for row in tables_result["rows"]]

        schema = {}

        for table in tables:

            describe_query = f"DESCRIBE {table}"

            columns = self.db.run_query(describe_query)

            schema[table] = columns["rows"]

        self.schema = schema

        return schema