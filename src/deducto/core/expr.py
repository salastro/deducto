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

class And(Expr):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        left_str = str(self.left) if isinstance(self.left, Var) or isinstance(self.left, Not) else f"({self.left})"
        right_str = str(self.right) if isinstance(self.right, Var) or isinstance(self.right, Not) else f"({self.right})"
        return f"{left_str} ∧ {right_str}"

    def __eq__(self, other):
        if not isinstance(other, And):
            return False
        return self.left == other.left and self.right == other.right

class Or(Expr):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        left_str = str(self.left) if isinstance(self.left, Var) or isinstance(self.left, Not) else f"({self.left})"
        right_str = str(self.right) if isinstance(self.right, Var) or isinstance(self.right, Not) else f"({self.right})"
        return f"{left_str} ∨ {right_str}"

    def __eq__(self, other):
        if not isinstance(other, Or):
            return False
        return self.left == other.left and self.right == other.right

class Implies(Expr):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        left_str = str(self.left) if isinstance(self.left, Var) or isinstance(self.left, Not) else f"({self.left})"
        right_str = str(self.right) if isinstance(self.right, Var) or isinstance(self.right, Not) else f"({self.right})"
        return f"{left_str} → {right_str}"

    def __eq__(self, other):
        if not isinstance(other, Implies):
            return False
        return self.left == other.left and self.right == other.right

class Iff(Expr):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        left_str = str(self.left) if isinstance(self.left, Var) or isinstance(self.left, Not) else f"({self.left})"
        right_str = str(self.right) if isinstance(self.right, Var) or isinstance(self.right, Not) else f"({self.right})"
        return f"{left_str} ↔ {right_str}"

    def __eq__(self, other):
        if not isinstance(other, Iff):
            return False
        return self.left == other.left and self.right == other.right

class Xor(Expr):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        left_str = str(self.left) if isinstance(self.left, Var) or isinstance(self.left, Not) else f"({self.left})"
        right_str = str(self.right) if isinstance(self.right, Var) or isinstance(self.right, Not) else f"({self.right})"
        return f"{left_str} ⊕ {right_str}"

    def __eq__(self, other):
        if not isinstance(other, Xor):
            return False
        return self.left == other.left and self.right == other.right

class TrueExpr(Expr):
    def __init__(self):
        pass

    def __str__(self):
        return "𝗧"

    def __eq__(self, other):
        if not isinstance(other, TrueExpr):
            return False
        return True

class FalseExpr(Expr):
    def __init__(self):
        pass

    def __str__(self):
        return "𝗙"

    def __eq__(self, other):
        if not isinstance(other, FalseExpr):
            return False
        return True
