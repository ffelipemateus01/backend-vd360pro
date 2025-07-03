from pydantic import BaseModel
from typing import List

class Node(BaseModel):
     id: int
     label: str
     color: str

class Connection(BaseModel):
     from_node_id: int
     to_node_id: int

class Flowchart(BaseModel):
     nodes: List[Node]
     connections: List[Connection]