import requests
import datetime;import time
import os
from dotenv import load_dotenv
import pprint
class DataGrab:
    def __init__(self):
        load_dotenv(dotenv_path=".env")
        self.link = os.environ.get("link")
        self.email = os.environ.get("email")
        self.alertlist = []
        self.incidentlist = []
        self.ioclist = []

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
                        self.ioclist.append([incident.get("incidentId",""),
                                             entity_type,
                                             item])
                self.incidentlist.append([alert.get("alertId",""),
                                        incident.get("incidentId",""),
                                        incident.get("severity",""),
                                        incident.get("status",""),
                                        incident.get("createdTime",""),])
    
                self.alertlist.append([alert.get("alertId",""),
                                        incident.get("incidentId",""),
                                        alert.get("machineId",""),
                                        alert.get("detectionSource",""),
                                        alert.get("firstActivity","")])