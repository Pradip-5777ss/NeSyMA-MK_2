import os
from src.orchestrator import NeuroSymbolicOrchestrator

def main():
    print("[INFO] Initializing Neuro-Symbolic Orchestrator for Phase 3 E2E Test...")
    orchestrator = NeuroSymbolicOrchestrator()
    
    # Using calc_1.py as the test subject
    legacy_file_path = "data/calc_1.py"
    
    if not os.path.exists(legacy_file_path):
        print(f"[ERROR] Test file {legacy_file_path} not found.")
        return
        
    print(f"\n[INFO] Starting End-to-End Pipeline on {legacy_file_path}")
    success = orchestrator.run_pipeline(legacy_file_path, max_retries=3)
    
    if success:
        print("\n[SUCCESS] Phase 3 End-to-End Test Completed Successfully!")
    else:
        print("\n[FAILURE] Phase 3 End-to-End Test Failed.")

if __name__ == "__main__":
    main()
