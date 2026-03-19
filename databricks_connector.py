from databricks import sql


class DatabricksConnector:

    def __init__(self, server_hostname, http_path, access_token):

        self.connection = sql.connect(
            server_hostname=server_hostname,
            http_path=http_path,
            access_token=access_token
        )

    def normalize_query(self, query):

        q = query.strip()

        if q.endswith(";"):
            q = q[:-1]

        upper = q.upper()

        if upper.startswith("SHOW") or upper.startswith("DESCRIBE"):
            q = q.replace("LIMIT 100", "")

        return q

    def run_query(self, query):

        query = self.normalize_query(query)

        print("Executing SQL:", query)

        with self.connection.cursor() as cursor:

            cursor.execute(query)

            columns = [c[0] for c in cursor.description]

            rows = cursor.fetchall()

        return {
            "columns": columns,
            "rows": rows
        }