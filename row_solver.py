
import itertools
from pysmt.shortcuts import Symbol, Bool, And, Or, Not, Implies, Iff
from pysmt.shortcuts import Solver, is_sat, get_model, get_atoms

class RowFormula:

    def __init__(self, dimension):
        self.dimension = dimension
        self.environment = None
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

        # print(half_disjunction_formula)

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

        # print(neighbor_conjunction_formula)

        # The full formula for a row or column of size self.dimension
        self.full_formula = And([half_disjunction_formula, neighbor_conjunction_formula])

    def assign_value(self, index, val):
        if val == '1':
            self.full_formula = And([self.full_formula, self.var_list[index]])
        elif val == '0':
            self.full_formula = And([self.full_formula, Not(self.var_list[index])])

    def is_satisfiable(self):
        """
        Method
        :return True if the formula is satisfiable
        """
        return is_sat(self.full_formula)

    def get_all_solutions(self, base_formula):
        """
        Method
        :return True if the formula has more than one solution
        """
        if not is_sat(base_formula):
            return []

        model = get_model(base_formula)

        # Block the found solution to find the other solutions
        first_sol_blocker = Or([Not(Iff(var, model[var])) for var in self.var_list])
        new_formula = And([base_formula, first_sol_blocker])
        return [model] + self.get_all_solutions(new_formula)

    def get_solution(self):
        """
        Method
        for formulas with a unique solution returns the values
        """
        solutions = self.get_all_solutions(self.full_formula)

        def get_common(var, sols):
            if len(sols) == 0:
                return '_'
            first_sol = ('1' if sols[0][var] == Bool(True) else '0')         
            if len(sols) == 1:
                return first_sol
            elif len(sols) > 1:
                if first_sol == get_common(var, sols[1:]):
                    return first_sol
                else:
                    return '_'

        partial_solution = []
        # find common elements
        for var in self.var_list:
            partial_solution.append(get_common(var, solutions))
        
        return partial_solution 

    def get_atoms(self):
        return get_atoms(self.full_formula)

    def fill_in(self, values):
        self.environment = values
        if len(values) == self.dimension:
            for i in range(0, self.dimension):
                if values[i] != '_':
                    self.assign_value(i, values[i])
        else:
            print("Array of values does not match dimension")


if __name__ == "__main__":
    row = RowFormula(8)
    env = ['0', '1', '1', '0', '_', '_', '1', '_']
    row.fill_in(env)
    print("My formula is satisfiable: ", row.is_satisfiable())
    solution = row.get_solution()
    if solution == env:
        print('no progress made with:', env)
    else:
        print('env:', env, '\nsol:', solution)
