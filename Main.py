from Lexical_Analyzer import LexicalAnalyzer
from ParserLogic import Parser
from semantic import SemanticAnalyzer
from codegen import CodeGenerator
from ast_nodes import IfStatement, Assignment, BinOp, Variable, Number

def print_ast(node, level=0):
    indent = "  " * level
    if isinstance(node, IfStatement):
        print(f"{indent}IfStatement")
        print(f"{indent}  Condition:")
        print_ast(node.condition, level + 2)
        print(f"{indent}  Then Body:")
        for stmt in node.then_body:
            print_ast(stmt, level + 2)
        if node.else_body:
            print(f"{indent}  Else Body:")
            for stmt in node.else_body:
                print_ast(stmt, level + 2)
    elif isinstance(node, Assignment):
        print(f"{indent}Assignment: {node.name} = ...")
        print_ast(node.value, level + 2)
    elif isinstance(node, BinOp):
        print(f"{indent}BinOp: {node.op}")
        print_ast(node.left, level + 2)
        print_ast(node.right, level + 2)
    elif isinstance(node, Variable):
        print(f"{indent}Variable: {node.name}")
    elif isinstance(node, Number):
        print(f"{indent}Number: {node.value}")
    else:
        print(f"{indent}Unknown Node: {node}")

# Sample Code to Compile
# Note: ParserLogic only parses a single IF statement.
# We assume 'x' is defined in the environment.
source_code = """
if (x > 5) {
    y = 10;
} else {
    y = 0;
}
"""

print("=== 1. Source Code ===")
print(source_code.strip())
print("\n")

# --- PHASE 1: LEXICAL ANALYSIS ---
print("=== 2. Tokens (Lexical Analysis) ===")
lexer = LexicalAnalyzer(source_code)
tokens = lexer.tokenize()
for t in tokens:
    print(t)
print("\n")

# --- PHASE 2: SYNTAX ANALYSIS ---
print("=== 3. Parse Tree (Syntax Analysis) ===")
# Remove EOF token for Parser if necessary, or Parser handles it?
# LexicalAnalyzer appends EOF. ParserLogic checks self.pos < len(tokens).
# Let's try passing tokens directly.
parser = Parser(tokens)
ast = parser.parse()
print_ast(ast)
print("\n")

# --- PHASE 3: SEMANTIC ANALYSIS ---
print("=== 4. Semantic Checks ===")
semantic_analyzer = SemanticAnalyzer()

# Pre-define 'x' to simulate a global scope where x was previously declared
print("LOG: Pre-defining variable 'x' in symbol table.")
semantic_analyzer.symbol_table['x'] = 'int'

semantic_analyzer.visit(ast)
print("Semantic Analysis Passed: Symbol Table =", semantic_analyzer.symbol_table)
print("\n")

# --- PHASE 4: CODE GENERATION ---
print("=== 5. Generated Target Code ===")
codegen = CodeGenerator()
codegen.visit(ast)
target_code = codegen.get_output()
print(target_code)
