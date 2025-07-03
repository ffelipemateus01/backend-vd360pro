from api.controls.flowchart.models import Flowchart, Node, Connection

list_nodes = [Node(id=0, label='Felipe', color='Blue'), Node(id=1, label='Mateus', color='Red')]
list_connections = [Connection(from_node_id=0, to_node_id=1)]
flowchart = Flowchart(nodes=list_nodes, connections=list_connections)

def altera_fluxograma():
    flow = flowchart.model_dump_json()
    print(flow)