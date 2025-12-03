import sys
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

print("Enter your source code (Press Ctrl+D to finish):")
source_code = sys.stdin.read()

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
# ParserLogic expects a single IF statement (starting with 'if')
parser = Parser(tokens)
try:
    ast = parser.parse()
    print_ast(ast)
    print("\n")
except Exception as e:
    print(f"Parsing Error: {e}")
    sys.exit(1)

# --- PHASE 3: SEMANTIC ANALYSIS ---
print("=== 4. Semantic Checks ===")
semantic_analyzer = SemanticAnalyzer()

# HACK: The provided ParserLogic only supports parsing a single IF statement,
# preventing variable declarations (Assignments) prior to the IF block.
# To allow testing variables in the condition (e.g., if x > 5), we pre-define
# a set of common variables in the symbol table.
print("LOG: Pre-defining variables 'a'-'z' in symbol table for testing (Parser limitation).")
for char_code in range(ord('a'), ord('z') + 1):
    semantic_analyzer.symbol_table[chr(char_code)] = 'int'

try:
    semantic_analyzer.visit(ast)
    print("Semantic Analysis Passed: Symbol Table =", semantic_analyzer.symbol_table)
    print("\n")
except ValueError as e:
    print(f"Semantic Error: {e}")
    sys.exit(1)

# --- PHASE 4: CODE GENERATION ---
print("=== 5. Generated Target Code ===")
codegen = CodeGenerator()
codegen.visit(ast)
target_code = codegen.get_output()
print(target_code)
