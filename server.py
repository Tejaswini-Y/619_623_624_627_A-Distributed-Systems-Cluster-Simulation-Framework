from flask import Flask, jsonify
from node_manager import NodeManager

app = Flask(__name__)
node_manager = NodeManager()

@app.route('/add_node', methods=['POST'])
def add_node():
    node = node_manager.add_node()
    return jsonify(node), 201

@app.route('/list_nodes', methods=['GET'])
def list_nodes():
    return jsonify(node_manager.list_nodes()), 200

@app.route('/')
def home():
    return jsonify({"message": "Node Manager API"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

