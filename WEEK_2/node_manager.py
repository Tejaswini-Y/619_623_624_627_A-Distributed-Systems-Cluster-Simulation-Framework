import docker
import random
import time
from pod_scheduler import PodScheduler  # Import the PodScheduler class

class NodeManager:
    def __init__(self):
        self.client = docker.from_env()
        self.nodes = {}
        self.heartbeats = {}
        self.pod_scheduler = PodScheduler(self)  # Create an instance of PodScheduler

    def add_node(self):
        """Creates a new Docker container to simulate a node and registers it."""
        node_id = f"node-{random.randint(1000, 9999)}"
        container = self.client.containers.run(
            "ubuntu",
            command="sleep infinity",
            detach=True,
            name=node_id
        )
        cpu_count = self.get_cpu_count(container)
        self.nodes[node_id] = {
            "container_id": container.id,
            "cpu_cores": cpu_count,
            "used_cpu": 0,
            "pods": []
        }
        self.heartbeats[node_id] = time.time()
        return {"node_id": node_id, "cpu_cores": cpu_count}

    def get_cpu_count(self, container):
        """Gets available CPU cores (simulated as 2 cores per node)."""
        return 2  

    def list_nodes(self):
        """Returns the registered nodes."""
        return self.nodes

    def receive_heartbeat(self, node_id):
        """Updates the last received heartbeat time for a node."""
        if node_id in self.nodes:
            self.heartbeats[node_id] = time.time()

    def detect_failed_nodes(self):
        """Detects nodes that have stopped sending heartbeats."""
        current_time = time.time()
        failed_nodes = [node_id for node_id, last_heartbeat in self.heartbeats.items()
                        if (current_time - last_heartbeat) > 10]
       
        for node_id in failed_nodes:
            self.pod_scheduler.reschedule_pods(node_id)  # Reschedule pods before removing node
            self.nodes.pop(node_id, None)
            self.heartbeats.pop(node_id, None)

        return failed_nodes

    def schedule_pod(self, pod_id, cpu_request=1, strategy="first_fit"):
        """Calls the PodScheduler to schedule a pod."""
        return self.pod_scheduler.schedule_pod(pod_id, cpu_request, strategy)  # Use the pod scheduler instance

