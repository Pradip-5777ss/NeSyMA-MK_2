import os
import sys

# Add src to the python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.verifier.json_reader import JSONASTLoader
from src.verifier.z3_translator import Z3Translator
from src.verifier.core_verifier import EquivalenceVerifier

def main():
    print("Initializing Phase 2: Symbolic Verifier Testing...\n")
    
    exports_dir = os.path.join(os.path.dirname(__file__), '..', 'data', 'exports')
    legacy_path = os.path.join(exports_dir, 'calc_1_ast.json')
    modern_path = os.path.join(exports_dir, 'calc_1_modern_mock.json')
    
    # 1. JSON Injection Bridge
    print(f"Loading Legacy AST: {legacy_path}")
    legacy_ast = JSONASTLoader.load(legacy_path)
    print(f"Loading Modern AST: {modern_path}")
    modern_ast = JSONASTLoader.load(modern_path)
    
    # 2. Arithmetic Translation Engine (with SSA Tracker and Variable Mapper)
    print("\nTranslating Legacy AST to Z3 Constraints...")
    legacy_translator = Z3Translator(prefix="L_")
    legacy_translator.translate(legacy_ast)
    
    print("Translating Modern AST to Z3 Constraints...")
    modern_translator = Z3Translator(prefix="M_")
    modern_translator.translate(modern_ast)
    
    # 3. Core Verifier Engine
    print("\nStarting Equivalence Prover...")
    verifier = EquivalenceVerifier()
    is_equiv, message = verifier.verify(legacy_translator, modern_translator)
    
    print(f"\nResult: {message}")
    if is_equiv:
        print("\n✅ Verification Passed: Formally Equivalent")
    else:
        print("\n❌ Verification Failed")

if __name__ == "__main__":
    main()
