from opcua import Client, ua
from datetime import datetime

class CNCDataFetcher:
    def __init__(self, client):
        self.client = client
        self.nodes = {}
        self.node_map = {
            "id": ua.NodeId(1007, 3),
            "machine": ua.NodeId(1008, 3),
            "spindle_speed": ua.NodeId(1009, 3),
            "temperature": ua.NodeId(1010, 3),
            "status": ua.NodeId(1011, 3),
            "timestamp": ua.NodeId(1012, 3),
        }

    def is_connected(self):
        try:
            self.client.get_node("i=84").get_value()
            return True
        except:
            return False

    def refresh_connection(self):
        if not self.is_connected():
            print(" Reconnecting OPC UA client...")
            try:
                self.client.disconnect()
            except:
                pass
            try:
                self.client.connect()
                print(" Reconnected OPC UA client successfully.")
            except Exception as e:
                print(" Failed to reconnect OPC UA client:", e)

    def resolve_nodes(self):
        try:
            self.nodes = {
                name: self.client.get_node(node_id)
                for name, node_id in self.node_map.items()
            }
        except Exception as e:
            self.nodes = {}
            return f"Failed to resolve nodes: {e}"
        return None

    def get_data(self):
        self.refresh_connection()

        if not self.nodes:
            error = self.resolve_nodes()
            if error:
                return {"Error": error}

        data = {}
        for name, node in self.nodes.items():
            if name in ["id", "machine", "timestamp"]:
                continue  # ✅ Skip these fields
            try:
                value = node.get_value()
                data[name] = value
            except Exception as e:
                data[name] = f"Error: {e}"

        return [data]  # ✅ Return a list for consistent format
