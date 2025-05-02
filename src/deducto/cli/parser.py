import re
from deducto.core.expr import *

TOKEN_SPEC = [
    (r'\s+', None),           # Skip whitespace
    (r'\(', 'LPAREN'),
    (r'\)', 'RPAREN'),
    (r'¬|!|~|NOT', 'NOT'),
    (r'∧|&|AND', 'AND'),
    (r'∨|\||OR', 'OR'),
    (r'→|->|IMPLIES', 'IMPLIES'),
    (r'↔|<->|IFF', 'IFF'),
    (r'⊕|\^|XOR', 'XOR'),
    (r'TRUE|T', 'TRUE'),
    (r'FALSE|F', 'FALSE'),
    (r'[A-Za-z_][A-Za-z0-9_]*', 'VAR'),
]

class Token:
    def __init__(self, type_, value):
        self.type = type_
        self.value = value
    def __repr__(self):
        return f'Token({self.type}, {self.value})'

def tokenize(text):
    regex_parts = [f'({pattern})' for pattern, _ in TOKEN_SPEC]
    regex = '|'.join(regex_parts)
    types = [type_ for _, type_ in TOKEN_SPEC]

    pos = 0
    while pos < len(text):
        match = re.match(regex, text[pos:])
        if not match:
            raise SyntaxError(f"Invalid token at position {pos}: '{text[pos]}'")

        for i, type_ in enumerate(types):
            value = match.group(i + 1)
            if value is not None:
                if type_ is not None:  # Skip whitespace
                    yield Token(type_, value)
                break

        pos += len(match.group(0))

class Parser:
    def __init__(self, tokens):
        self.tokens = list(tokens)
        self.pos = 0

    def peek(self):
        # Check the next token without advancing
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def advance(self):
        self.pos += 1

    def expect(self, type_):
        # Check the next token and advance if it matches the expected type
        # Made for bracket matching
        token = self.peek()
        if token and token.type == type_:
            self.advance()
            return token
        raise SyntaxError(f"Expected {type_} but got {token}")

    def parse(self):
        # Start parsing from the top-level expression
        return self.parse_iff()

    def parse_iff(self):
        node = self.parse_implies()
        while self.peek() and self.peek().type == 'IFF':
            self.advance()
            node = Iff(node, self.parse_implies())
        return node

    def parse_implies(self):
        node = self.parse_xor()
        while self.peek() and self.peek().type == 'IMPLIES':
            self.advance()
            node = Implies(node, self.parse_xor())
        return node

    def parse_xor(self):
        node = self.parse_or()
        while self.peek() and self.peek().type == 'XOR':
            self.advance()
            node = Xor(node, self.parse_or())
        return node

    def parse_or(self):
        node = self.parse_and()
        while self.peek() and self.peek().type == 'OR':
            self.advance()
            node = Or(node, self.parse_and())
        return node

    def parse_and(self):
        node = self.parse_not()
        while self.peek() and self.peek().type == 'AND':
            self.advance()
            node = And(node, self.parse_not())
        return node

    def parse_not(self):
        if self.peek() and self.peek().type == 'NOT':
            self.advance()
            return Not(self.parse_not())
        return self.parse_atom()

    def parse_atom(self):
        token = self.peek()
        if token is None:
            raise SyntaxError("Unexpected end of input")
        if token.type == 'VAR':
            self.advance()
            return Var(token.value)
        if token.type == 'LPAREN':
            self.advance()
            expr = self.parse()
            self.expect('RPAREN')
            return expr
        # Handle True and False literals
        if token.type == 'TRUE':
            self.advance()
            return TrueExpr()
        if token.type == 'FALSE':
            self.advance()
            return FalseExpr()
        raise SyntaxError(f"Unexpected token: {token}")

def parse(text: str) -> Expr:
    return Parser(tokenize(text)).parse()

if __name__ == '__main__':
    print(parse(input("Enter a logical expression: ")))
