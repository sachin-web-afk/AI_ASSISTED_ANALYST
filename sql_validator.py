class SQLValidator:

    def __init__(self, schema):
        pass

    def validate(self, query):

        if not query:
            raise Exception("Invalid query")

        q = query.lower()

        unsafe_keywords = ["drop", "delete", "truncate", "alter"]

        for word in unsafe_keywords:
            if word in q:
                raise Exception("Unsafe query detected")

        return query
    

