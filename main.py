from data import DataGrab as Data
from database import Database
data = Data()
db = Database(
    "mandatory.db",
    ("incidents", data.incidents.itemlist),
    ("alerts", data.alerts.itemlist),
    ("ioc", data.ioc.itemlist)
)
def execute():
    if __name__ == "__main__":
        data.get_token()
        data.get_incidents()
        data.incidents.Sorter()
        data.alerts.Sorter()
        data.ioc.Sorter()
    else:
        print("Not Running on main instance")

execute()