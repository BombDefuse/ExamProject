import requests
import datetime;import time
from sorting import ListCreator
import os
from dotenv import load_dotenv
class DataGrab:
    def __init__(self):
        load_dotenv(dotenv_path=".env")
        self.link = os.environ.get("link")
        self.email = os.environ.get("email")
        self.datalist = []
        self.alerts = ListCreator(itemlist=["alertId","incidentId","machineId","detectionSource","firstActivity", "value","entity"],dataInstance=self)
        self.incidents = ListCreator(itemlist=["alertId","incidentId","createdTime","machineId"],dataInstance=self)
        self.ioc = ListCreator(itemlist=["incidentid"],dataInstance=self)

    def get_token(self):
        try:
            self.token = requests.post(f"{self.link}/api/auth/token", json={"email":self.email}).json()["token"]
            print(self.token)
        except Exception as error:
            print(f"[Error] {error}")

    def get_incidents(self):
        try:
            self.response = requests.get(f"{self.link}/api/incidents?$top=100&$skip=0", headers={"Authorization": f"Bearer {self.token}"}).json()
            self.Create_List()
            time.sleep(1.5)
            while self.response.get("@odata.nextLink"):
                self.response = requests.get(f"{self.link}{self.response["@odata.nextLink"]}", headers={"Authorization": f"Bearer {self.token}"}).json()
                self.Create_List()
        except Exception as error:
            print(f"[Error] {error}")

    def Create_List(self):
        self.timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for incident in self.response["value"]:
            for alert in incident["alerts"]:
                for entity_type, entity_values in alert["entities"].items():
                    for item in entity_values:
                        print("type:", entity_type)
                        print("value:", item)
                        self.datalist.append({ 
                            "incidentId": incident["incidentId"],
                            "incidentName": incident["incidentName"],
                            "severity": incident["severity"],
                            "status": incident["status"],
                            "createdTime": incident["createdTime"],
                            "alertId": alert["alertId"],
                            "machineId": alert["machineId"],
                            "detectionSource": alert["detectionSource"],
                            "firstActivity": alert["firstActivity"],
                            "value": item,
                            "type": entity_type
                        })