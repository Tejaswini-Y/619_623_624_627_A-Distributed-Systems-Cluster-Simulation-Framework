class PodScheduler:
    def __init__(self, node_manager):
        self.node_manager = node_manager

    def schedule_pod(self, pod_id, cpu_request, strategy="first_fit"):
        """Schedules a pod based on the chosen strategy."""
        nodes = self.node_manager.nodes

        if strategy == "first_fit":
            suitable_nodes = [n for n in nodes if nodes[n]["cpu_cores"] - nodes[n]["used_cpu"] >= cpu_request]
            if suitable_nodes:
                selected_node = suitable_nodes[0]

        elif strategy == "best_fit":
            suitable_nodes = sorted(
                [n for n in nodes if nodes[n]["cpu_cores"] - nodes[n]["used_cpu"] >= cpu_request],
                key=lambda n: nodes[n]["cpu_cores"] - nodes[n]["used_cpu"]
            )
            selected_node = suitable_nodes[0] if suitable_nodes else None

        elif strategy == "worst_fit":
            suitable_nodes = sorted(
                [n for n in nodes if nodes[n]["cpu_cores"] - nodes[n]["used_cpu"] >= cpu_request],
                key=lambda n: nodes[n]["cpu_cores"] - nodes[n]["used_cpu"],
                reverse=True
            )
            selected_node = suitable_nodes[0] if suitable_nodes else None

        else:
            return None

        if selected_node:
            self.node_manager.nodes[selected_node]["used_cpu"] += cpu_request
            self.node_manager.nodes[selected_node]["pods"].append(pod_id)
            return {"pod_id": pod_id, "node_id": selected_node}

        return None

    def reschedule_pods(self, failed_node_id):
        """Reschedules pods from a failed node."""
        if failed_node_id not in self.node_manager.nodes:
            return
       
        failed_pods = self.node_manager.nodes[failed_node_id]["pods"]
        del self.node_manager.nodes[failed_node_id]

        for pod_id in failed_pods:
            self.schedule_pod(pod_id, 1, "first_fit")
