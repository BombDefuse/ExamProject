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
        self.incidents = ListCreator(itemlist=["alertId","incidentId","severity","status","createdTime"],dataInstance=self)
        self.alerts = ListCreator(itemlist=["alertId","incidentId","machineId","detectionSource","firstActivity"],dataInstance=self)
        self.ioc = ListCreator(itemlist=["incidentId","type","value"],dataInstance=self)

    def get_token(self):
        try:
            self.token = requests.post(f"{self.link}/api/auth/token", json={"email":self.email}).json()["token"]
        except Exception as error:
            print(f"[Error] {error}")

    def get_incidents(self):
        try:
            url = f"{self.link}/api/incidents?$top=100&$skip=0"
            while url:
                response = requests.get(url,headers={"Authorization": f"Bearer {self.token}"})
                if response.status_code != 200:
                    print(f"[Error] API returned {response.status_code}")
                    break
                self.response = response.json()#Needs to swap to json here to recieve status code
                self.Create_List()
                self.next_link = self.response.get("@odata.nextLink")
                url = f"{self.link}{self.next_link}" if self.next_link else None
                time.sleep(1.5)
        except Exception as error:
            print(f"[Error] {error}")

    def Create_List(self):
        self.timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for incident in self.response["value"]:
            for alert in incident["alerts"]:
                for entity_type, entity_values in alert["entities"].items():
                    for item in entity_values:
                        # print("type:", entity_type)
                        # print("value:", item)
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