from data import DataGrab as Data
from database import Database
data = Data()
db = Database(
    "mandatory.db",data,
     ("incidents", ["incidentId","incidentName","severity","status","createdtime"]),
     ("alerts", ["alertId","incidentId","machineId","detectionSource","firstActivity"]),
     ("ioc", ["incidentId","type","value"])
)
def execute():
    if __name__ == "__main__":
        data.get_token()
        data.get_incidents()
        db.Write_Database()
    else:
        print("Not Running on main instance")

execute()