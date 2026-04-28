import tree_sitter
import tree_sitter_python
import hashlib

class LegacyCodeParser:
    def __init__(self):
        # 4. Tree-sitter Language Binding
        self.language = tree_sitter.Language(tree_sitter_python.language())
        self.parser = tree_sitter.Parser(self.language)

    def parse(self, source_code: str) -> tree_sitter.Tree:
        """
        5. AST Extraction Script (Core Parser Engine)
        Parses legacy Python code (as text) into an Abstract Syntax Tree (AST).
        """
        if isinstance(source_code, str):
            source_code = source_code.encode('utf-8')
        return self.parser.parse(source_code)

    def visualize(self, node, depth=0):
        """
        8. AST Visualizer (Terminal Visualization)
        Prints the parsed tree beautifully in the terminal.
        """
        indent = "  " * depth
        print(f"{indent}{node.type} [{node.start_point[0]}:{node.start_point[1]} - {node.end_point[0]}:{node.end_point[1]}]")
        for child in node.children:
            self.visualize(child, depth + 1)

    def _get_tier(self, node_type: str) -> int:
        tier_1 = {'assignment', 'augmented_assignment', 'binary_operator', 'identifier', 'integer', 'float', 'return_statement'}
        tier_2 = {'if_statement', 'elif_clause', 'else_clause', 'comparison_operator', 'boolean_operator'}
        tier_3 = {'for_statement', 'while_statement'}
        
        if node_type in tier_1: return 1
        if node_type in tier_2: return 2
        if node_type in tier_3: return 3
        return 0

    def extract_logic(self, node, source_bytes):
        """
        6. Pattern Isolation (Logic Mapping & Rule Enforcement)
        Extracts mathematical logic and Control Flow, assigning unique deterministic IDs.
        Returns a dictionary representing the logical state structure.
        """
        # Positional Hashing for deterministic unique state ID
        state_string = f"{node.type}_{node.start_point[0]}_{node.start_point[1]}_{node.end_point[0]}_{node.end_point[1]}"
        state_id = hashlib.sha256(state_string.encode('utf-8')).hexdigest()[:12]

        result = {
            "id": f"state_{state_id}", # Deterministic unique label
            "type": node.type,
            "tier": self._get_tier(node.type),
            "text": node.text.decode('utf-8') if node.text else "",
            "start": node.start_point,
            "end": node.end_point,
            "children": []
        }

        # Traverse children to capture the structured tree with unique IDs.
        for child in node.children:
            if child.is_named:
                child_logic = self.extract_logic(child, source_bytes)
                result["children"].append(child_logic)

        return result
