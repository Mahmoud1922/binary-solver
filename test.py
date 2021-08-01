
from pysmt.shortcuts import Symbol, And, Not, is_sat

varA = Symbol("A") # Default type is Boolean
varB = Symbol("B")
f = And([varA, Not(varB)])
g = f.substitute({varB:varA})
    
res = is_sat(f)
assert res # SAT
print("f := %s is SAT? %s" % (f, res))

res = is_sat(g)
print("g := %s is SAT? %s" % (g, res))
assert not res # UNSAT