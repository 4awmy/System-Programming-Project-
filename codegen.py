from ast_nodes import *

class CodeGenerator:
    def __init__(self):
        self.instructions = []
        self.temp_counter = 0
        self.label_counter = 0

    def get_output(self):
        return "\n".join(self.instructions)

    def emit(self, instruction):
        self.instructions.append(instruction)

    def new_temp(self):
        self.temp_counter += 1
        return f"temp_{self.temp_counter}"

    def new_label(self, name):
        self.label_counter += 1
        return f"{name}_{self.label_counter}"

    def visit(self, node):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception(f'No visit_{type(node).__name__} method')

    def visit_Number(self, node):
        self.emit(f"LOADI {node.value}")

    def visit_Variable(self, node):
        self.emit(f"LOAD {node.name}")

    def visit_Assignment(self, node):
        self.visit(node.value)
        self.emit(f"STORE {node.name}")

    def visit_BinOp(self, node):
        # Accumulator-based logic for binary operations
        # 1. Evaluate Right operand -> Result in ACC
        self.visit(node.right)

        # 2. Store Right result in a temporary variable
        temp = self.new_temp()
        self.emit(f"STORE {temp}")

        # 3. Evaluate Left operand -> Result in ACC
        self.visit(node.left)

        # 4. Perform Operation with Temp (Left OP Right)
        op_map = {
            '+': 'ADD',
            '-': 'SUB',
            '*': 'MUL',
            '/': 'DIV',
            '>': 'CMP',
            '<': 'CMP',
            '==': 'CMP',
            '>=': 'CMP',
            '<=': 'CMP',
            '!=': 'CMP'
        }

        instruction = op_map.get(node.op, "UNKNOWN_OP")
        self.emit(f"{instruction} {temp}")

    def visit_IfStatement(self, node):
        else_label = self.new_label("else_label")
        end_label = self.new_label("end_label")

        # Condition
        self.visit(node.condition)
        self.emit(f"JMP_FALSE {else_label}")

        # Then Body
        for stmt in node.then_body:
            self.visit(stmt)
        self.emit(f"JMP {end_label}")

        # Else Label
        self.emit(f"{else_label}:")

        # Else Body
        if node.else_body:
            for stmt in node.else_body:
                self.visit(stmt)

        # End Label
        self.emit(f"{end_label}:")
