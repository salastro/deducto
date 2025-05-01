class Expr:
    def __str__(self):
        """
        Returns a string stresentation of the object.
        """
        return self.__class__.__name__

class Var(Expr):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    def __eq__(self, other):
        if not isinstance(other, Var):
            return False
        return self.name == other.name

class Not(Expr):
    def __init__(self, negated):
        self.negated = negated

    def __str__(self):
        if isinstance(self.negated, Var):
            return f"¬{self.negated}"
        return f"¬({self.negated})"

    def __eq__(self, other):
        if not isinstance(other, Not):
            return False
        return self.negated == other.negated

class BinaryOperation(Expr):
    INFIX_SYMBOL = None # to define in the child classes

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        left_str = str(self.left) if isinstance(self.left, (Var, Not)) else f"({self.left})"
        right_str = str(self.right) if isinstance(self.right, (Var, Not)) else f"({self.right})"
        return f"{left_str} {self.INFIX_SYMBOL} {right_str}"

    def __eq__(self, other):
        if not isinstance(other, type(self)): # not the same type
            return False
        return self.left == other.left and self.right == other.right

class And(BinaryOperation):
    INFIX_SYMBOL = "∧"

class Or(BinaryOperation):
    INFIX_SYMBOL = "∨"

class Implies(BinaryOperation):
    INFIX_SYMBOL = "→"

class Iff(BinaryOperation):
    INFIX_SYMBOL = "↔"

class Xor(BinaryOperation):
    INFIX_SYMBOL = "⊕"

class ConstantExpr(Expr):
    INFIX_SYMBOL = None
    def __init__(self):
        pass

    def __str__(self):
        return str(self.INFIX_SYMBOL)

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False
        return True

class TrueExpr(ConstantExpr):
    INFIX_SYMBOL = "𝗧"

class FalseExpr(ConstantExpr):
    INFIX_SYMBOL = "𝗙"
