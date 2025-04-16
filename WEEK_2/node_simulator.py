import requests
import time

SERVER_URL = "http://localhost:5000"

def send_heartbeats():
    """Continuously sends heartbeat signals for all registered nodes, including newly added ones."""
    while True:
        try:
            # Fetch the latest list of nodes
            response = requests.get(f"{SERVER_URL}/list_nodes")
            nodes = response.json()
            NODE_IDS = list(nodes.keys())  # Get updated node IDs

            if not NODE_IDS:
                print("No nodes found! Please add at least one node.")
            else:
                for node_id in NODE_IDS:
                    requests.post(f"{SERVER_URL}/heartbeat", json={"node_id": node_id})
                    print(f"Heartbeat sent for {node_id}")

        except Exception as e:
            print(f"Failed to send heartbeat: {e}")

        time.sleep(5)  # Send heartbeats every 5 seconds

if __name__ == "__main__":
    print("Starting node heartbeat simulation...")
    send_heartbeats()
