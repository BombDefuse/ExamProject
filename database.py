import sqlite3 as sql
class Database:
    def __init__(self,name,data_instance,*tables):
        self.data = data_instance
        self.conn = sql.connect(name)
        self.cursor = self.conn.cursor()

        for name, columns in tables:
            self.query = f"""
                CREATE TABLE IF NOT EXISTS {name} (
                    {', '.join(f'{col} TEXT NOT NULL' for col in columns)},
                    UNIQUE ({', '.join(columns)})
                )
            """
            print(f"Created table: {name}")
            print(self.query)
            self.cursor.execute(self.query)
        self.conn.commit()
    def Write_Database(self):
        print(self.data.alertlist)
        print(self.data.incidentlist)
        print(self.data.ioclist)