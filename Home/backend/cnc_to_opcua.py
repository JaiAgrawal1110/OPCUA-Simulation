from opcua import Client, ua
from pymongo import MongoClient, errors as pymongo_errors
import mysql.connector
import time
import threading


# MongoDB to OPC UA Handler
class MongoToOPCUAHandler:
    def __init__(self):
        self.client = Client("opc.tcp://localhost:53530/OPCUA/SimulationServer")
        self.mongo_client = MongoClient("mongodb://localhost:27017/")
        self.collection = self.mongo_client["CNC_DATA"]["Machine_status"]
        self.NODES = {
            "SpindleSpeed": "ns=3;i=1009",
            "Temperature": "ns=3;i=1010",
            "Status": "ns=3;i=1011"
        }
        self.running = False
        self.thread = None
        self.last_id = None

    def start(self):
        if self.running:
            print("MongoToOPCUAHandler already running.")
            return
        try:
            self.client.connect()
            print("Connected to OPC UA server (MongoDB).")
        except Exception as e:
            print("MongoDB OPC UA connect error:", e)
            return
        self.running = True
        self.thread = threading.Thread(target=self.run)
        self.thread.start()

    def stop(self):
        self.running = False
        if self.thread and self.thread.is_alive():
            self.thread.join()
            print("Mongo OPC UA thread stopped.")
        try:
            self.client.disconnect()
            print("Disconnected from OPC UA server (MongoDB).")
        except Exception as e:
            print("MongoDB client disconnect error:", e)

    def run(self):
        while self.running:
            try:
                query = {} if not self.last_id else {"_id": {"$gt": self.last_id}}
                documents = list(self.collection.find(query).sort("_id", 1))

                if not documents:
                    print("No new MongoDB records.")
                    time.sleep(2)
                    continue

                for doc in documents:
                    if not self.running:
                        break
                    self.last_id = doc["_id"]
                    spindle = doc.get("spindle_speed", 0.0)
                    temp = doc.get("temperature", 0.0)
                    status = doc.get("status", "Idle")

                    print(f"[MongoDB] → Spindle: {spindle}, Temp: {temp}, Status: {status}")
                    self._write_to_opcua(spindle, temp, status)
                    time.sleep(2)

            except pymongo_errors.PyMongoError as e:
                print("MongoDB read error:", e)
                time.sleep(2)

    def _write_to_opcua(self, spindle, temp, status):
        try:
            self.client.get_node(self.NODES["SpindleSpeed"]).set_value(
                ua.Variant(float(spindle), ua.VariantType.Double))
            self.client.get_node(self.NODES["Temperature"]).set_value(
                ua.Variant(float(temp), ua.VariantType.Double))
            self.client.get_node(self.NODES["Status"]).set_value(
                ua.Variant(str(status), ua.VariantType.String))
        except Exception as e:
            print("OPC UA write error (MongoDB):", e)


# MySQL to OPC UA Handler
class MySQLToOPCUAHandler:
    def __init__(self):
        self.client = Client("opc.tcp://localhost:53530/OPCUA/SimulationServer")
        self.NODES = {
            "SpindleSpeed": "ns=3;i=1009",
            "Temperature": "ns=3;i=1010",
            "Status": "ns=3;i=1011"
        }
        self.running = False
        self.thread = None
        self.last_id = 0
        self.db = None
        self.cursor = None

    def start(self):
        if self.running:
            print("MySQLToOPCUAHandler already running.")
            return
        try:
            self.client.connect()
            print("Connected to OPC UA server (MySQL).")
        except Exception as e:
            print("MySQL OPC UA connect error:", e)
            return

        try:
            self.db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Renu-9694",
                database="opcua"
            )
            self.cursor = self.db.cursor(dictionary=True)
        except mysql.connector.Error as e:
            print("MySQL DB connection error:", e)
            return

        self.running = True
        self.thread = threading.Thread(target=self.run)
        self.thread.start()

    def stop(self):
        self.running = False
        if self.thread and self.thread.is_alive():
            self.thread.join()
            print("MySQL OPC UA thread stopped.")
        try:
            self.client.disconnect()
            print("Disconnected from OPC UA server (MySQL).")
        except Exception as e:
            print("MySQL client disconnect error:", e)

        if self.cursor:
            self.cursor.close()
        if self.db:
            self.db.close()

    def run(self):
        while self.running:
            try:
                self.cursor.execute("SELECT * FROM machine_data WHERE id > %s ORDER BY id ASC", (self.last_id,))
                rows = self.cursor.fetchall()

                if not rows:
                    print("No new MySQL records.")
                    time.sleep(2)
                    continue

                for row in rows:
                    if not self.running:
                        break
                    self.last_id = row["id"]
                    spindle = row.get("spindle_speed", 0.0)
                    temp = row.get("temp", 0.0)
                    status = row.get("status", "Idle")

                    print(f"[MySQL] → Spindle: {spindle}, Temp: {temp}, Status: {status}")
                    self._write_to_opcua(spindle, temp, status)
                    time.sleep(2)

            except mysql.connector.Error as e:
                print("MySQL read error:", e)
                time.sleep(2)

    def _write_to_opcua(self, spindle, temp, status):
        try:
            self.client.get_node(self.NODES["SpindleSpeed"]).set_value(
                ua.Variant(float(spindle), ua.VariantType.Double))
            self.client.get_node(self.NODES["Temperature"]).set_value(
                ua.Variant(float(temp), ua.VariantType.Double))
            self.client.get_node(self.NODES["Status"]).set_value(
                ua.Variant(str(status), ua.VariantType.String))
        except Exception as e:
            print("OPC UA write error (MySQL):", e)
