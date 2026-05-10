import z3
import re

class Z3Translator:
    """
    Translates AST JSON dicts into Z3 constraints.
    Features:
    - Symbolic Variable Mapper: Uses z3.Real/z3.Int.
    - SSA State Tracker: Handles reassignment by versioning variables.
    - Arithmetic Translation Engine.
    - Edge Case Constraints.
    """

    def __init__(self, prefix=""):
        self.prefix = prefix
        self.env = {} # Maps variable name -> current SSA version (int)
        self.vars = {} # Maps SSA variable name -> z3 object
        self.constraints = []
        self.edge_case_constraints = []
        self.final_return = None

    def _get_or_create_var(self, name: str):
        """Gets current SSA version of a variable or creates version 0."""
        if name not in self.env:
            self.env[name] = 0
            ssa_name = f"{self.prefix}{name}_0"
            self.vars[ssa_name] = z3.Real(ssa_name)
        
        ssa_name = f"{self.prefix}{name}_{self.env[name]}"
        return self.vars[ssa_name]

    def _increment_var(self, name: str):
        """Increments the SSA version of a variable, creating a new Z3 object."""
        if name not in self.env:
            self.env[name] = 0
        else:
            self.env[name] += 1
            
        ssa_name = f"{self.prefix}{name}_{self.env[name]}"
        self.vars[ssa_name] = z3.Real(ssa_name)
        return self.vars[ssa_name]

    def translate(self, node: dict):
        """Recursively translates the AST node to populate constraints."""
        node_type = node.get("type")
        
        if node_type in ["module", "block"]:
            for child in node.get("children", []):
                self.translate(child)
                
        elif node_type == "function_definition":
            # For verification, we just want to translate the body of the function.
            # We initialize parameters as version 0.
            for child in node.get("children", []):
                if child.get("type") == "parameters":
                    for param in child.get("children", []):
                        if param.get("type") == "identifier":
                            self._get_or_create_var(param.get("text"))
                elif child.get("type") == "block":
                    self.translate(child)
                    
        elif node_type == "expression_statement":
            for child in node.get("children", []):
                self.translate(child)
                
        elif node_type == "assignment":
            children = node.get("children", [])
            if len(children) >= 2:
                lhs_node = children[0]
                rhs_node = children[1]
                
                # Evaluate RHS first (using current versions of vars)
                rhs_expr = self._eval_expr(rhs_node)
                
                if lhs_node.get("type") == "identifier":
                    var_name = lhs_node.get("text")
                    new_z3_var = self._increment_var(var_name)
                    # Create the constraint: new_var == rhs_expr
                    self.constraints.append(new_z3_var == rhs_expr)
                    
        elif node_type == "return_statement":
            children = node.get("children", [])
            if children:
                self.final_return = self._eval_expr(children[0])

    def _eval_expr(self, node):
        """Evaluates an expression node and returns a Z3 expression/value."""
        node_type = node.get("type")
        text = node.get("text", "")
        
        if node_type == "identifier":
            return self._get_or_create_var(text)
            
        elif node_type in ["float", "integer", "number"]:
            return float(text)
            
        elif node_type == "parenthesized_expression":
            children = node.get("children", [])
            if children:
                # Evaluate the inner expression
                return self._eval_expr(children[0])
            return None
            
        elif node_type == "binary_operator":
            children = node.get("children", [])
            if len(children) >= 2:
                left_node = children[0]
                right_node = children[1]
                
                left_expr = self._eval_expr(left_node)
                right_expr = self._eval_expr(right_node)
                
                # Find the operator robustly
                left_text = left_node.get("text", "")
                right_text = right_node.get("text", "")
                
                # Try to extract the operator by removing the operands from the text
                op_text = text
                if text.startswith(left_text) and text.endswith(right_text):
                    op_text = text[len(left_text):-len(right_text)].strip()
                else:
                    # Fallback regex search if text format is a bit weird
                    if "+" in text: op_text = "+"
                    elif "-" in text: op_text = "-"
                    elif "*" in text: op_text = "*"
                    elif "/" in text: op_text = "/"
                
                if op_text == "+": return left_expr + right_expr
                elif op_text == "-": return left_expr - right_expr
                elif op_text == "*": return left_expr * right_expr
                elif op_text == "/":
                    # Edge Case Safety Rules (Div by Zero)
                    self.edge_case_constraints.append(right_expr != 0)
                    return left_expr / right_expr
                    
        return None
