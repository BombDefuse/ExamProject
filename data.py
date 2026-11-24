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
                for attempts in range(4):
                    response = requests.get(url,headers={"Authorization": f"Bearer {self.token}"})
                    if response.status_code != 200:
                        print(f"[Error] API returned {response.status_code}")
                    self.response = response.json()#Needs to swap to json here to recieve status code
                    self.Create_List()
                    self.next_link = self.response.get("@odata.nextLink")
                    if self.next_link:
                        url = f"{self.link}{self.next_link}"
                    else:
                        url = None
                    time.sleep(1.5)
            else:
                print(f"[Error] Maximum tries of {attempts} reached")
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
                            "incidentId": incident.get("incidentId",""),
                            "incidentName": incident.get("incidentName",""),
                            "severity": incident.get("severity",""),
                            "status": incident.get("status",""),
                            "createdTime": incident.get("createdTime",""),
                            "alertId": alert.get("alertId",""),
                            "machineId": alert.get("machineId",""),
                            "detectionSource": alert.get("detectionSource",""),
                            "firstActivity": alert.get("firstActivity",""),
                            "value": item,
                            "type": entity_type
                        })