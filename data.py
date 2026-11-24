import requests
import datetime;import time
from database import Database
from sorting import ListCreator
import os
from dotenv import load_dotenv

class DataGrab:
    def __init__(self):
        self.link = os.environ.get("link")
        self.email = os.environ.get("email")
        self.datalist = []
        self.alerts = ListCreator(itemlist=["alertId","incidentId","machineId","detectionSource","firstActivity"],dataInstance=self)
        self.id = ListCreator(itemlist=["alertId","incidentId","createdTime","machineId"],dataInstance=self)

    def get_token(self):
        try:
            self.token = requests.post(f"{self.link}/api/auth/token", json={"email":self.email}).json()["token"]
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
                for items in alert["entities"]:
                    print(alert["entities"][items])
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
                        #ToDo: any entity that can come (ips,domains,fileHashes,processes,url)
                    })