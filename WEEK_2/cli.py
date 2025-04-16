import requests

SERVER_URL = "http://localhost:5000"

def safe_request(method, url, json=None):
    """Handles API requests safely"""
    try:
        response = requests.request(method, url, json=json)
        response.raise_for_status()
        
        if response.text:  # Ensure response is not empty
            return response.json()
        else:
            return {"error": "Empty response from server"}
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

def add_node():
    """Add a new node to the cluster"""
    print(safe_request("POST", f"{SERVER_URL}/add_node"))

def list_nodes():
    """List all nodes in the cluster"""
    print(safe_request("GET", f"{SERVER_URL}/list_nodes"))

def send_heartbeat():
    """Send heartbeat to keep node alive"""
    node_id = input("Enter Node ID: ")
    print(safe_request("POST", f"{SERVER_URL}/heartbeat", json={"node_id": node_id}))

def schedule_pod():
    """Schedule a new pod with given ID and CPU request"""
    pod_id = input("Enter Pod ID: ")
    
    try:
        cpu_request = int(input("Enter CPU request (default 1): ") or 1)
    except ValueError:
        print("Invalid input! CPU request set to 1.")
        cpu_request = 1
    
    strategy = input("Enter scheduling strategy (first_fit/best_fit/worst_fit): ") or "first_fit"

    print(safe_request("POST", f"{SERVER_URL}/schedule_pod", json={
        "pod_id": pod_id,
        "cpu_request": cpu_request,
        "strategy": strategy
    }))

def list_pods():
    """List all scheduled pods"""
    print(safe_request("GET", f"{SERVER_URL}/list_pods"))

def delete_node():
    """Delete a node from the cluster"""
    node_id = input("Enter Node ID to delete: ")
    print(safe_request("POST", f"{SERVER_URL}/delete_node", json={"node_id": node_id}))

def main():
    while True:
        print("\n **Distributed Cluster CLI**")
        print("1. Add Node")
        print("2. List Nodes")
        print("3. Send Heartbeat")
        print("4. Schedule Pod")
        print("5. List Pods")
        print("6. Delete Node")
        print("7. Exit")
        
        choice = input("\nEnter your choice: ")

        if choice == "1":
            add_node()
        elif choice == "2":
            list_nodes()
        elif choice == "3":
            send_heartbeat()
        elif choice == "4":
            schedule_pod()
        elif choice == "5":
            list_pods()
        elif choice == "6":
            delete_node()
        elif choice == "7":
            print("Exiting CLI...")
            break
        else:
            print("Invalid choice, try again!")

if __name__ == "__main__":
    main()

