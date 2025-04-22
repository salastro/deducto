import re
from deducto.expr import *

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
    (r'[A-Za-z_][A-Za-z0-9_]*', 'VAR'),
]

class Token:
    def __init__(self, type_, value):
        self.type = type_
        self.value = value
    def __repr__(self):
        return f'Token({self.type}, {self.value})'

def tokenize(text):
    regex = '|'.join(f'({pattern})' for pattern, _ in TOKEN_SPEC) # create an "or" regex from patterns
    types = [type_ for _, type_ in TOKEN_SPEC]
    for match in re.finditer(regex, text): # find all non-overlapping matches
        for i, type_ in enumerate(types):
            # check if match is not None to skip whitespace
            # match.group(i + 1) cause group(0) is the whole match
            if type_ and match.group(i + 1):
                yield Token(type_, match.group(i + 1)) # return match without terminating function
                break

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
        raise SyntaxError(f"Unexpected token: {token}")

def parse(text):
    return Parser(tokenize(text)).parse()

if __name__ == '__main__':
    print(parse(input("Enter a logical expression: ")))
