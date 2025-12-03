import re
#===============================
# 1.Lexical Analysis
#===============================
class Token:
    def __init__(self, type_, value):
        self.type = type_
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, '{self.value}')"

class LexicalAnalyzer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.tokens = []

    def tokenize(self):
        token_specs = [
            ('IF', r'\bif\b'),  # 'if' keyword
            ('ELSE', r'\belse\b'),  # 'else' keyword
            ('NUMBER', r'\d+'),  # Integer number
            ('ID', r'[a-zA-Z_]\w*'),  # Identifiers
            ('OP', r'==|!=|<=|>=|<|>'),  # Comparison operators
            ('ASSIGN', r'='),  # Assignment operator
            ('SEMI', r';'),  # Semicolon
            ('LPAREN', r'\('),  # (
            ('RPAREN', r'\)'),  # )
            ('LBRACE', r'\{'),  # {
            ('RBRACE', r'\}'),  # }
            ('SKIP', r'[ \t\n]+'),  # Skip whitespace
            ('MISMATCH', r'.'),  # Any other character
        ]

        tok_regex =  '|'.join('(?P<%s>%s)' % pair for pair in token_specs)

        for mo in re.finditer(tok_regex, self.text):
            kind = mo.lastgroup
            value = mo.group()

            if kind == 'SKIP':
                continue
            elif kind == 'MISMATCH':
                raise RuntimeError(f"Lexical Error: Unexpected character {value!r}")

            token = Token(kind, value)
            self.tokens.append(token)
            print(f"[Found Token] Type: {kind:<10} Value: {value}")

        self.tokens.append(Token('EOF', None))
        return self.tokens