## WEEK 1 
* Implement API Server base implementation and Node Manager functionality and add a node  
*  First run server.py file (python3 server.py) and then run commands:
    * **curl -X POST http://localhost:5000/add_node**
    * **curl -X GET http://localhost:5000/list_nodes**

## WEEK 2
* Implement Pod Scheduler and Health Monitor with node heartbeat mechanism
* First run server.py (python3 server.py) and the add nodes.
* Next to check the heartbeat of the nodes run node_simulator.py(python3 node_simulator.py)
* To schedule a pod run the command
    * **curl -X POST http://localhost:5000/schedule_pod -H "Content-Type: application/json" -d '{"pod_id": "pod-1", "cpu_request": 1, "strategy": "first_fit"}'**
    * **curl -X GET http://localhost:5000/list_pods** [This is for listing the pods made, and to see which nodes it has been assigned to]
* Next step is to delete a node, and rescedule the pod to another node
    * **curl -X POST http://localhost:5000/delete_node -H "Content-Type: application/json" -d '{"node_id": "node-<node_id>"}'**
    * **curl -X GET http://localhost:5000/list_pods**
* Finally, pod will be rescheduled to a different node and if a node doesn't have any pods, it will be deleted with no pod rescheduling.

## WEEK 3
* Nodes are being added correctly.
* Pods are scheduled properly.
* Health monitoring works as expected.
* Failure detection and recovery are handled.
