from deducto.expr import *
from deducto.rules.inference import *
from deducto.rules.equivalence import *

p = Var("P")
q = Var("Q")
r = Var("R")
s = Var("S")

premise = right = And(p, q)
left = And(r, s)
implication = Implies(right, left)

print("Variables:", p, q, r)
print("Modus Ponens:")
print("Premise:", premise)
print("Implication:", implication)
modus_ponens_conclusion = modus_ponens(implication, premise)
print("Conclusion:", modus_ponens_conclusion)

print()

print("Simplification:")
print("Conjunction:", modus_ponens_conclusion)
simplification_conclusion = simplification(modus_ponens_conclusion)
print("Conclusion:", simplification_conclusion)

print()

premise = And(p, And(q, r))

print("Premise:", premise)
print("Commutative And:")
commutative_and_conclusion = commutative_and(premise)
print("Conclusion:", commutative_and_conclusion)

print("Associative And:")
associative_and_conclusion = associative_and(commutative_and_conclusion)
print("Conclusion:", associative_and_conclusion)
