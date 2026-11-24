import sqlite3 as sql

class Database:
    def __init__(self, api_instance):
        #Stores the api instance as variable instance and then saves that as self.api similar to self.link = link
        self.api = api_instance
        self.query = """
        CREATE TABLE IF NOT EXISTS incidents (
            id INTEGER PRIMARY KEY NOT NULL,
            alertID TEXT NOT NULL,
            incidentId TEXT NOT NULL,
            category TEXT NOT NULL,
            domain TEXT NOT NULL,
            machineID TEXT NOT NULL,
            firstSeen TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            detectionSource TEXT NOT NULL,

            UNIQUE (
                alertID, incidentId, category, domain,
                machineID, firstSeen, detectionSource
            )
        )
        """
        self.conn = sql.connect("mandatory.db")
        self.c = self.conn.cursor()
        self.c.execute(self.query)

    def write_table(self):
        try:
            self.c.executemany("INSERT OR IGNORE INTO incidents (alertID, IncidentId, category, domain, machineID,firstSeen,timestamp,detectionsource) VALUES (?,?,?,?,?,?,?,?)", self.api.data)
            self.conn.commit()
        except Exception as e:
            print(f"[Error]: {e}")
            self.conn.rollback()
        finally:
            self.c.close()
            self.conn.close()