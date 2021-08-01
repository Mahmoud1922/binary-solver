
import itertools
from pysmt.shortcuts import Symbol, Bool, And, Or, Not, Implies
from pysmt.shortcuts import Solver, is_sat

class RowFormula:

    def __init__(self, dimension):
        self.dimension = dimension
        # Create variable list
        self.var_list = []
        for i in range(1,self.dimension+1):
            self.var_list.append(Symbol("A"+str(i)))

        print(self.var_list)

        # Create formulae satisfiable iff exactly half the symbols are true and half are false
        negation_combinations = list(itertools.combinations(set(self.var_list), int(self.dimension / 2)))
        half_disjunction_formula = Bool(False)
        for negation_comb in negation_combinations:
            intact_comb = set(self.var_list).difference(set(negation_comb))
            half_formula_conjunction = And([And([var for var in intact_comb]),And([Not(var) for var in negation_comb])])
            half_disjunction_formula = Or([half_disjunction_formula, half_formula_conjunction])

        print(half_disjunction_formula)

        # Create formulae satisfiable if at most two neighbors have the same logical value
        # Formula expressed for neighboring triples
        neighbor_conjunction_formula = Bool(True)
        for i in range(0,self.dimension-2):
            neighbor_subformula = And(
                [Implies(And([self.var_list[i], self.var_list[i+1]]), Not(self.var_list[i+2])),
                Implies(And([Not(self.var_list[i]), Not(self.var_list[i+1])]), self.var_list[i+2]),
                Implies(And([self.var_list[i+1], self.var_list[i+2]]), Not(self.var_list[i])),
                Implies(And([Not(self.var_list[i+1]), Not(self.var_list[i+2])]), self.var_list[i])])
            neighbor_conjunction_formula = And([neighbor_conjunction_formula, neighbor_subformula])

        print(neighbor_conjunction_formula)

        # The full formula for a row or column of size self.dimension
        self.full_formula = And([half_disjunction_formula, neighbor_conjunction_formula])

    def is_satisfiable(self):
        return is_sat(self.full_formula)

# res = is_sat(f)
# assert res # SAT
# print("f := %s is SAT? %s" % (f, res))

# res = is_sat(g)
# print("g := %s is SAT? %s" % (g, res))
# assert not res # UNSAT

if __name__ == "__main__":
    row = RowFormula(6)
    print("My formula is satisfiable: ", row.is_satisfiable())
