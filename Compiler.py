import re
# ==========================================
# 1. LEXICAL ANALYSIS (The Tokenizer)
# ==========================================
class Token:
    def __init__(self, type_, value):
        self.type = type_
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, {repr(self.value)})"
#====================================================
# 1.1 Lexical Operation Class
#====================================================
class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.tokens = []

    def tokenize(self):
        # A list that contains the tokens for the IF condition syntax
        token_specification = [
            ('IF', r'\bif\b'),  # if keyword
            ('ELSE', r'\belse\b'),  # else keyword
            ('NUMBER', r'\d+'),  # Integer number
            ('ID', r'[a-zA-Z_][a-zA-Z0-9_]*'),  # Identifiers
            ('OP', r'==|!=|<=|>=|<|>'),  # Comparison operators
            ('ASSIGN', r'='),  # Assignment operator
            ('SEMI', r';'),  # Semicolon
            ('LPAREN', r'\('),  # (
            ('RPAREN', r'\)'),  # )
            ('LBRACE', r'\{'),  # {
            ('RBRACE', r'\}'),  # }
            ('SKIP', r'[ \t\n]+'),  # Skip over spaces and tabs
            ('MISMATCH', r'.'),  # Any other character
        ]

        tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)

        print(f"\n--- 1. Lexical Analysis (Tokenizing: '{self.text}') ---")

        for mo in re.finditer(tok_regex, self.text):
            kind = mo.lastgroup
            value = mo.group()

            if kind == 'SKIP':
                continue
            elif kind == 'MISMATCH':
                raise RuntimeError(f'Lexical Error: Unexpected character {value!r}')

            token = Token(kind, value)
            self.tokens.append(token)
            print(f"  [Found Token] Type: {kind:<10} Value: {value}")

        self.tokens.append(Token('EOF', None))  # End of file marker
        return self.tokens
# ==========================================
# 2. SYNTAX ANALYSIS (The Parser)
# ==========================================
class ASTNode:
    """Base class for all Abstract Syntax Tree nodes"""
    pass


class ProgramNode(ASTNode):
    def __init__(self, statements):
        self.statements = statements


class IfNode(ASTNode):
    def __init__(self, condition, then_branch, else_branch=None):
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch


class AssignmentNode(ASTNode):
    def __init__(self, identifier, value):
        self.identifier = identifier
        self.value = value


class ConditionNode(ASTNode):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current_token(self):
        return self.tokens[self.pos]

    def eat(self, token_type):
        """Consumes the current token if it matches the expected type."""
        if self.current_token().type == token_type:
            self.pos += 1
        else:
            raise SyntaxError(f"Expected {token_type}, got {self.current_token().type}")

    def parse(self):
        return self.parse_program()

    def parse_program(self):
        statements = []
        while self.current_token().type != 'EOF':
            statements.append(self.parse_statement())
        return ProgramNode(statements)

    def parse_statement(self):
        token = self.current_token()
        if token.type == 'IF':
            return self.parse_if()
        elif token.type == 'ID':
            return self.parse_assignment()
        else:
            raise SyntaxError(f"Unexpected token in statement: {token}")

    def parse_assignment(self):
        # ID = NUMBER ;
        id_token = self.current_token()
        self.eat('ID')
        self.eat('ASSIGN')
        value_token = self.current_token()
        self.eat('NUMBER')
        self.eat('SEMI')
        return AssignmentNode(id_token.value, value_token.value)

    def parse_if(self):
        # if ( condition ) { statements } else { statements }
        self.eat('IF')
        self.eat('LPAREN')
        condition = self.parse_condition()
        self.eat('RPAREN')

        self.eat('LBRACE')
        then_stmts = []
        while self.current_token().type != 'RBRACE':
            then_stmts.append(self.parse_statement())
        self.eat('RBRACE')

        else_stmts = None
        if self.current_token().type == 'ELSE':
            self.eat('ELSE')
            self.eat('LBRACE')
            else_stmts = []
            while self.current_token().type != 'RBRACE':
                else_stmts.append(self.parse_statement())
            self.eat('RBRACE')

        return IfNode(condition, then_stmts, else_stmts)

    def parse_condition(self):
        # ID OP NUMBER
        left = self.current_token()
        self.eat('ID')
        op = self.current_token()
        self.eat('OP')
        right = self.current_token()
        self.eat('NUMBER')
        return ConditionNode(left.value, op.value, right.value)


# ==========================================
# 3. SEMANTIC ANALYSIS
# ==========================================
class SemanticAnalyzer:
    def __init__(self):
        # A simple symbol table to track declared variables
        self.symbol_table = set()

    def analyze(self, node):
        """Recursively checks the AST for semantic errors."""
        if isinstance(node, ProgramNode):
            print("LOG: Semantic Analysis - Checking Program...")
            for stmt in node.statements:
                self.analyze(stmt)

        elif isinstance(node, AssignmentNode):
            # When we assign to a variable, we add it to the symbol table
            print(f"LOG: Semantic Analysis - Variable '{node.identifier}' defined/updated.")
            self.symbol_table.add(node.identifier)

        elif isinstance(node, IfNode):
            self.analyze(node.condition)
            for stmt in node.then_branch:
                self.analyze(stmt)
            if node.else_branch:
                for stmt in node.else_branch:
                    self.analyze(stmt)

        elif isinstance(node, ConditionNode):
            # Check if the variable used in condition exists
            if node.left not in self.symbol_table:
                # In a real compiler, this would be an error.
                # For this demo, we'll just warn.
                print(f"WARNING: Semantic Error - Variable '{node.left}' used in IF condition before assignment!")
            else:
                print(f"LOG: Semantic Analysis - Condition variable '{node.left}' is valid.")


# ==========================================
# 4. CODE GENERATION (Bonus)
# ==========================================
class CodeGenerator:
    def __init__(self):
        self.label_counter = 0

    def new_label(self):
        self.label_counter += 1
        return f"L{self.label_counter}"

    def generate(self, node):
        if isinstance(node, ProgramNode):
            code = ""
            for stmt in node.statements:
                code += self.generate(stmt)
            return code

        elif isinstance(node, AssignmentNode):
            # Simple 3-address like code
            return f"MOV {node.identifier}, {node.value}\n"

        elif isinstance(node, IfNode):
            else_label = self.new_label()
            end_label = self.new_label()

            # Generate condition code
            # "IF_FALSE condition GOTO else_label"
            code = self.generate(node.condition)
            code += f"JMP_FALSE {else_label}\n"

            # Then block
            for stmt in node.then_branch:
                code += self.generate(stmt)
            code += f"JMP {end_label}\n"

            # Else block
            code += f"{else_label}:\n"
            if node.else_branch:
                for stmt in node.else_branch:
                    code += self.generate(stmt)

            code += f"{end_label}:\n"
            return code

        elif isinstance(node, ConditionNode):
            # Example: CMP x, 10
            return f"CMP {node.left}, {node.right}\n"