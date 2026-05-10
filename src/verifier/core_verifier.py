import z3

class EquivalenceVerifier:
    """
    Core Verifier Engine (The Equivalence Prover).
    Receives Z3 expressions/constraints from the legacy and modern code
    and uses the Z3 theorem prover to check if they are mathematically equivalent.
    """

    def __init__(self):
        self.solver = z3.Solver()

    def verify(self, legacy_translator, modern_translator):
        """
        Verifies equivalence by asserting that the outputs can be DIFFERENT.
        If the solver returns unsat (Unsatisfiable), no such inputs exist,
        thus the codes are mathematically equivalent.
        
        Args:
            legacy_translator (Z3Translator): Translator containing legacy constraints.
            modern_translator (Z3Translator): Translator containing modern constraints.
            
        Returns:
            tuple: (is_equivalent, message)
        """
        # 1. Add all logic constraints and edge cases from legacy code
        for constraint in legacy_translator.constraints:
            self.solver.add(constraint)
        for ec in legacy_translator.edge_case_constraints:
            self.solver.add(ec)

        # 2. Add all logic constraints and edge cases from modern code
        for constraint in modern_translator.constraints:
            self.solver.add(constraint)
        for ec in modern_translator.edge_case_constraints:
            self.solver.add(ec)

        # 3. Link input parameters (assuming version 0 in both are the inputs)
        for name in legacy_translator.env:
            if name in modern_translator.env:
                l_var_name = f"{legacy_translator.prefix}{name}_0"
                m_var_name = f"{modern_translator.prefix}{name}_0"
                
                l_var = legacy_translator.vars.get(l_var_name)
                m_var = modern_translator.vars.get(m_var_name)
                
                if l_var is not None and m_var is not None:
                    self.solver.add(l_var == m_var)

        # 4. Assert that their return values are DIFFERENT
        if legacy_translator.final_return is not None and modern_translator.final_return is not None:
            self.solver.add(legacy_translator.final_return != modern_translator.final_return)
        else:
            return False, "Missing return statements in one or both ASTs."

        # 5. Check satisfiability
        result = self.solver.check()
        
        if result == z3.unsat:
            return True, "Formally Equivalent"
        elif result == z3.sat:
            model = self.solver.model()
            return False, f"Counterexample found: {model}"
        else:
            return False, "Solver returned unknown"
