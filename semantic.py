from ast_nodes import *

class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = {}

    def visit(self, node):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception(f'No visit_{type(node).__name__} method')

    def visit_Number(self, node):
        pass

    def visit_Variable(self, node):
        if node.name not in self.symbol_table:
            raise ValueError(f"Variable '{node.name}' is not defined.")

    def visit_Assignment(self, node):
        self.visit(node.value)
        self.symbol_table[node.name] = "int"  # Default type as requested

    def visit_BinOp(self, node):
        self.visit(node.left)
        self.visit(node.right)

    def visit_IfStatement(self, node):
        self.visit(node.condition)
        for stmt in node.then_body:
            self.visit(stmt)
        if node.else_body:
            for stmt in node.else_body:
                self.visit(stmt)
