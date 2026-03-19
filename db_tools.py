class DBTools:

    def __init__(self, db):
        self.db = db


    def create_table(self, sql):

        if not sql.lower().startswith("create"):
            return {"error": "Only CREATE TABLE allowed"}

        return self.db.run_query(sql)


    def insert_record(self, sql):

        if not sql.lower().startswith("insert"):
            return {"error": "Only INSERT allowed"}

        return self.db.run_query(sql)


    def update_record(self, sql):

        if not sql.lower().startswith("update"):
            return {"error": "Only UPDATE allowed"}

        return self.db.run_query(sql)


    def select_data(self, sql):

        if not sql.lower().startswith("select"):
            return {"error": "Only SELECT allowed"}

        return self.db.run_query(sql)