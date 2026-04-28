import tree_sitter
import tree_sitter_python
import uuid

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

    def extract_logic(self, node, source_bytes):
        """
        6. Pattern Isolation (Logic Mapping & Rule Enforcement)
        Extracts mathematical logic and Control Flow, assigning unique IDs.
        Returns a dictionary representing the logical state structure.
        """
        result = {
            "id": str(uuid.uuid4()), # Project's Critical Rule: Unique label for every logical state
            "type": node.type,
            "text": node.text.decode('utf-8') if node.text else "",
            "start": node.start_point,
            "end": node.end_point,
            "children": []
        }

        # Filter children based on important control flow or math operations
        # For simplicity, we keep relevant nodes, e.g., expressions, statements, control structures
        for child in node.children:
            # We can refine this logic to specifically target math & control flow,
            # but initially we capture the structured tree with unique IDs.
            if child.is_named:
                child_logic = self.extract_logic(child, source_bytes)
                result["children"].append(child_logic)

        return result
