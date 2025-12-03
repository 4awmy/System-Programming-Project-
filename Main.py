from Compiler import Lexer, Parser, SemanticAnalyzer, CodeGenerator, ProgramNode

def print_ast(node, level=0):
    indent = "  " * level
    if isinstance(node, ProgramNode):
        print(f"{indent}Program")
        for stmt in node.statements:
            print_ast(stmt, level + 1)
    elif hasattr(node, 'identifier') and hasattr(node, 'value'): # Assignment
        print(f"{indent}Assignment: {node.identifier} = {node.value}")
    elif hasattr(node, 'condition'): # If
        print(f"{indent}If Statement")
        print(f"{indent}  Condition: {node.condition.left} {node.condition.op} {node.condition.right}")
        print(f"{indent}  Then Block:")
        for stmt in node.then_branch:
            print_ast(stmt, level + 3)
        if node.else_branch:
            print(f"{indent}  Else Block:")
            for stmt in node.else_branch:
                print_ast(stmt, level + 3)

# Sample Code to Compile
# This code contains an assignment, then an IF check using that variable
source_code = """
x = 10;
y = 20;
if (x > 5) {
    z = 100;
} else {
    z = 0;
}
"""

print("=== 1. Source Code ===")
print(source_code.strip())
print("\n")

# --- PHASE 1: LEXICAL ANALYSIS ---
print("=== 2. Tokens (Lexical Analysis) ===")
lexer = Lexer(source_code)
tokens = lexer.tokenize()
for t in tokens:
    print(t)
print("\n")

# --- PHASE 2: SYNTAX ANALYSIS ---
print("=== 3. Parse Tree (Syntax Analysis) ===")
parser = Parser(tokens)
ast = parser.parse()
print_ast(ast)
print("\n")

# --- PHASE 3: SEMANTIC ANALYSIS ---
print("=== 4. Semantic Checks ===")
semantic_analyzer = SemanticAnalyzer()
semantic_analyzer.analyze(ast)
print("\n")

# --- PHASE 4: CODE GENERATION (BONUS) ---
print("=== 5. Generated Target Code ===")
codegen = CodeGenerator()
target_code = codegen.generate(ast)
print(target_code)