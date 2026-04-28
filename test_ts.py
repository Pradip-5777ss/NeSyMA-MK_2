import tree_sitter
import tree_sitter_python
try:
    lang = tree_sitter.Language(tree_sitter_python.language())
    parser = tree_sitter.Parser(lang)
    print("Success with Language object")
except Exception as e:
    print(f"Failed Language object: {e}")
    parser = tree_sitter.Parser(tree_sitter_python.language())
    print("Success with direct lang function")
