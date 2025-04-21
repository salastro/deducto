from abc import ABC, abstractmethod

class Expr(ABC):
    @abstractmethod
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

class Not(Expr):
    def __init__(self, operand):
        self.operand = operand

    def __str__(self):
        if isinstance(self.operand, Var):
            return f"¬{self.operand}"
        return f"¬({self.operand})"

class And(Expr):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        left_str = str(self.left) if isinstance(self.left, Var) else f"({self.left})"
        right_str = str(self.right) if isinstance(self.right, Var) else f"({self.right})"
        return f"{left_str} ∧ {right_str}"

class Or(Expr):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        left_str = str(self.left) if isinstance(self.left, Var) else f"({self.left})"
        right_str = str(self.right) if isinstance(self.right, Var) else f"({self.right})"
        return f"{left_str} ∨ {right_str}"

class Implies(Expr):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        left_str = str(self.left) if isinstance(self.left, Var) else f"({self.left})"
        right_str = str(self.right) if isinstance(self.right, Var) else f"({self.right})"
        return f"{left_str} → {right_str}"

class IFF(Expr):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        left_str = str(self.left) if isinstance(self.left, Var) else f"({self.left})"
        right_str = str(self.right) if isinstance(self.right, Var) else f"({self.right})"
        return f"{left_str} ↔ {right_str}"

class Xor(Expr):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        left_str = str(self.left) if isinstance(self.left, Var) else f"({self.left})"
        right_str = str(self.right) if isinstance(self.right, Var) else f"({self.right})"
        return f"{left_str} ⊕ {right_str}"

class TrueExpr(Expr):
    def __init__(self):
        pass

    def __str__(self):
        return "T"

class FalseExpr(Expr):
    def __init__(self):
        pass

    def __str__(self):
        return "F"
