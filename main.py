from data import DataGrab as Data
data = Data()
def execute():
    if __name__ == "__main__":
        data.get_token()
        data.get_incidents()
        data.alerts.Sorter()
    else:
        print("Not Running on main instance")

execute()