import docker
import random

class NodeManager:
    def __init__(self):
        self.client = docker.from_env()
        self.nodes = {}

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
            "cpu_cores": cpu_count
        }
        return {"node_id": node_id, "cpu_cores": cpu_count}

    def get_cpu_count(self, container):
        """Gets available CPU cores (for simulation, returning 2 cores)."""
        return 2  # Simulating 2 CPU cores per node

    def list_nodes(self):
        """Returns the registered nodes."""
        return self.nodes
