from flask import Flask, request, jsonify
import threading
from flask import render_template
import time
from node_manager import NodeManager
from pod_scheduler import PodScheduler

app = Flask(__name__)
node_manager = NodeManager()
pod_scheduler = PodScheduler(node_manager)

HEARTBEAT_TIMEOUT = 10  # Time in seconds before a node is considered failed

def health_monitor():
    """Monitors node heartbeats and reschedules pods if a node fails."""
    while True:
        time.sleep(HEARTBEAT_TIMEOUT)
        failed_nodes = node_manager.detect_failed_nodes()
        for node_id in failed_nodes:
            pod_scheduler.reschedule_pods(node_id)

threading.Thread(target=health_monitor, daemon=True).start()

@app.route('/add_node', methods=['POST'])
def add_node():
    node = node_manager.add_node()
    return jsonify(node), 201

@app.route('/list_nodes', methods=['GET'])
def list_nodes():
    return jsonify(node_manager.list_nodes()), 200

@app.route('/heartbeat', methods=['POST'])
def heartbeat():
    data = request.json
    node_id = data.get('node_id')
    node_manager.receive_heartbeat(node_id)
    print(f"Heartbeat received from node: {node_id}")
    return jsonify({"message": f"Heartbeat received from {node_id}"}), 200

@app.route('/schedule_pod', methods=['POST'])
def schedule_pod():
    data = request.json
    pod_id = data.get('pod_id')
    cpu_request = data.get('cpu_request', 1)
    strategy = data.get('strategy', 'first_fit')  # Default to First-Fit

    result = pod_scheduler.schedule_pod(pod_id, cpu_request, strategy)
    if result:
        return jsonify(result), 201
    else:
        return jsonify({"error": "No suitable node found"}), 400

@app.route('/list_pods', methods=['GET'])
def list_pods():
    all_pods = {node_id: data["pods"] for node_id, data in node_manager.nodes.items()}
    return jsonify(all_pods), 200

@app.route('/delete_node', methods=['POST'])
def delete_node():
    data = request.json
    node_id = data.get('node_id')

    if node_id not in node_manager.nodes:
        return jsonify({"error": "Node not found"}), 404

    # Get the pods from the deleted node
    pods_to_reschedule = node_manager.nodes[node_id]["pods"]

    # Remove node from tracking
    node_manager.nodes.pop(node_id, None)
    node_manager.heartbeats.pop(node_id, None)

    # Try stopping/removing the Docker container (if applicable)
    try:
        container = node_manager.client.containers.get(node_id)
        container.stop()
        container.remove()
    except Exception:
        pass  # Ignore errors if container doesn't exist

    if pods_to_reschedule:  # If there are pods to reschedule
        for pod_id in pods_to_reschedule:
            node_manager.schedule_pod(pod_id, cpu_request=1, strategy="first_fit")
        return jsonify({"message": f"Node {node_id} deleted and pods rescheduled"}), 200
    else:
        return jsonify({"message": f"Node {node_id} deleted. No pods to reschedule."}), 200

    
@app.route('/heartbeat_page')
def heartbeat_page():
    return render_template('heartbeat.html')

@app.route('/')
@app.route('/dashboard')
def dashboard():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
