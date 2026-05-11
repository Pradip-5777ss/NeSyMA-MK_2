import time
import os

from src.parser.core_parser import LegacyCodeParser
from src.verifier.z3_translator import Z3Translator
from src.verifier.core_verifier import EquivalenceVerifier
from src.neural.llm_provider import GeminiProvider
from src.neural.refactor_agent import NeuralRefactorer
from src.neural.metrics_logger import log_metrics

class NeuroSymbolicOrchestrator:
    def __init__(self):
        self.parser = LegacyCodeParser()
        self.verifier = EquivalenceVerifier()
        self.llm_provider = GeminiProvider()
        self.refactorer = NeuralRefactorer(self.llm_provider)

    def _read_file(self, filepath: str) -> str:
        with open(filepath, 'r') as f:
            return f.read()
            
    def _write_file(self, filepath: str, content: str):
        with open(filepath, 'w') as f:
            f.write(content)

    def run_pipeline(self, legacy_file_path: str, max_retries: int = 3):
        print(f"[INFO] Starting pipeline for {legacy_file_path}")
        legacy_code = self._read_file(legacy_file_path)
        
        print("[INFO] Parsing Legacy Code...")
        legacy_ast = self.parser.parse(legacy_code)
        
        # Translate legacy AST to Z3 constraints
        print("[INFO] Translating legacy code to Z3 constraints...")
        legacy_dict = self.parser.extract_logic(legacy_ast.root_node, legacy_code.encode('utf-8'))
        legacy_translator = Z3Translator(prefix="L_")
        legacy_translator.translate(legacy_dict)
        
        attempt = 0
        previous_errors = None
        final_code = None
        status = "Failed"
        
        total_llm_time_ms = 0
        total_z3_time_ms = 0
        
        while attempt < max_retries:
            attempt += 1
            print(f"\n[INFO] Attempt {attempt}/{max_retries}")
            
            # Step 1: LLM Refactoring
            print("[INFO] Requesting LLM Refactor...")
            start_llm = time.time()
            try:
                modern_code = self.refactorer.refactor(legacy_code, previous_errors)
            except Exception as e:
                print(f"[ERROR] LLM Request failed: {e}")
                previous_errors = str(e)
                continue
                
            llm_time_ms = (time.time() - start_llm) * 1000
            total_llm_time_ms += llm_time_ms
            
            # Optional: save intermediate output
            modern_file_path = legacy_file_path.replace(".py", f"_modern_attempt_{attempt}.py")
            self._write_file(modern_file_path, modern_code)
            
            # Step 2: Parse Modern Code
            print("[INFO] Parsing Modern Code...")
            modern_ast = self.parser.parse(modern_code)
            
            # Step 3: Translate to Z3 constraints
            print("[INFO] Translating modern code to Z3 constraints...")
            modern_dict = self.parser.extract_logic(modern_ast.root_node, modern_code.encode('utf-8'))
            modern_translator = Z3Translator(prefix="M_")
            try:
                modern_translator.translate(modern_dict)
            except Exception as e:
                print(f"[WARN] Translation failed: {e}")
                previous_errors = f"Translation error: {e}"
                continue
                
            # Step 4: Verify Equivalence
            print("[INFO] Verifying with Z3...")
            start_z3 = time.time()
            # Verify creates a new solver session inside EquivalenceVerifier but 
            # our current EquivalenceVerifier modifies self.solver state, so we need a fresh verifier
            verifier = EquivalenceVerifier()
            is_equivalent, message = verifier.verify(legacy_translator, modern_translator)
            z3_time_ms = (time.time() - start_z3) * 1000
            total_z3_time_ms += z3_time_ms
            
            if is_equivalent:
                print(f"[SUCCESS] Verification passed: {message}")
                final_code = modern_code
                status = "Success"
                
                # Save final verified code
                final_path = legacy_file_path.replace(".py", "_modern.py")
                self._write_file(final_path, final_code)
                print(f"[INFO] Verified code saved to {final_path}")
                
                break
            else:
                print(f"[FAIL] Verification failed: {message}")
                previous_errors = message

        # Log metrics
        metrics = {
            "file": legacy_file_path,
            "total_attempts_needed": attempt,
            "llm_generation_time_ms": total_llm_time_ms,
            "z3_verification_time_ms": total_z3_time_ms,
            "final_status": status
        }
        log_metrics(metrics)
        print(f"\n[INFO] Pipeline finished with status: {status}")
        return status == "Success"
