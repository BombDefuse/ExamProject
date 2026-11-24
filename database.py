import sqlite3 as sql
class Database:
    def __init__(self, name,*tables):
        self.conn = sql.connect(name)
        self.cursor = self.conn.cursor()

        for name, columns in tables:
            query = f"""
                CREATE TABLE IF NOT EXISTS {name} (
                    {', '.join(f'{col} TEXT NOT NULL' for col in columns)},
                    UNIQUE ({', '.join(columns)})
                )
            """

            print(f"Creating table: {name}")
            print(query)

            self.cursor.execute(query)

        self.conn.commit()