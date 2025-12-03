import dataclasses
from typing import List, Optional

@dataclasses.dataclass
class Node:
    pass

@dataclasses.dataclass
class Number(Node):
    value: int

@dataclasses.dataclass
class Variable(Node):
    name: str

@dataclasses.dataclass
class BinOp(Node):
    left: Node
    op: str
    right: Node

@dataclasses.dataclass
class Assignment(Node):
    name: str
    value: Node

@dataclasses.dataclass
class IfStatement(Node):
    condition: Node
    then_body: List[Node]
    else_body: Optional[List[Node]]