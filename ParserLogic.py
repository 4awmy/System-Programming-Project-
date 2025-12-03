from ast_nodes import IfStatement, BinOp, Variable, Number, Assignment
from Lexical_Analyzer import LexicalAnalyzer, Token


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.current_token = self.tokens[self.pos]

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.pos += 1
            if self.pos < len(self.tokens):
                self.current_token = self.tokens[self.pos]
        else:
            raise Exception(f"Syntax Error: Expected {token_type}, found {self.current_token.type}")

    def parse(self):
        """Entry point for the parser"""
        return self.parse_if_statement()

    def parse_if_statement(self):
        # if ( condition ) { block } else { block }
        self.eat('IF')
        self.eat('LPAREN')
        condition = self.parse_condition()
        self.eat('RPAREN')

        self.eat('LBRACE')
        then_body = self.parse_block()
        self.eat('RBRACE')

        else_body = None
        if self.current_token.type == 'ELSE':
            self.eat('ELSE')
            self.eat('LBRACE')
            else_body = self.parse_block()
            self.eat('RBRACE')

        return IfStatement(condition, then_body, else_body)

    def parse_condition(self):
        # ID OP (ID | NUMBER)
        left = Variable(self.current_token.value)
        self.eat('ID')

        op = self.current_token.value
        self.eat('OP')

        right = None
        if self.current_token.type == 'ID':
            right = Variable(self.current_token.value)
            self.eat('ID')
        elif self.current_token.type == 'NUMBER':
            right = Number(int(self.current_token.value))
            self.eat('NUMBER')

        return BinOp(left, op, right)

    def parse_block(self):
        # Simple block parser: looks for assignments like 'x = 5;'
        statements = []
        while self.current_token.type == 'ID':
            var_name = self.current_token.value
            self.eat('ID')
            self.eat('ASSIGN')

            value_node = None
            if self.current_token.type == 'NUMBER':
                value_node = Number(int(self.current_token.value))
                self.eat('NUMBER')
            elif self.current_token.type == 'ID':
                value_node = Variable(self.current_token.value)
                self.eat('ID')

            self.eat('SEMI')
            statements.append(Assignment(var_name, value_node))

        return statements


# --- Test Runner ---
if __name__ == "__main__":
    code = "if (x > 10) { y = 5; } else { y = 0; }"
    print(f"Testing Code: {code}")

    # 1. Lexical Analysis
    lexer = LexicalAnalyzer(code)
    tokens = lexer.tokenize()

    # 2. Syntax Analysis
    parser = Parser(tokens)
    ast = parser.parse()

    print("\nAbstract Syntax Tree (AST):")
    print(ast)