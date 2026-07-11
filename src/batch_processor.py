import os
import time
import json
import shutil
from typing import List

from src.orchestrator import NeuroSymbolicOrchestrator

class BatchProcessor:
    def __init__(self, source_dir: str, target_dir: str):
        self.orchestrator = NeuroSymbolicOrchestrator()
        self.source_dir = os.path.abspath(source_dir)
        self.target_dir = os.path.abspath(target_dir)
        self.failed_files = []
        self.report_path = "data/failed_files_report.json"

    def process_files(self, files: List[str]):
        """
        Iterates over a list of files and processes them through the orchestrator.
        Implements rate limiting and resilient error handling.
        """
        print(f"[INFO] Starting batch processing of {len(files)} files...")
        
        # Ensure target directory exists
        if os.path.exists(self.target_dir):
            shutil.rmtree(self.target_dir)
        os.makedirs(self.target_dir, exist_ok=True)
        
        # Ensure data directory exists for report
        os.makedirs("data", exist_ok=True)

        processed_count = 0

        for file_path in files:
            file_path = os.path.abspath(file_path)
            # Calculate the mirrored output path
            rel_path = os.path.relpath(file_path, self.source_dir)
            mirrored_dest_path = os.path.join(self.target_dir, rel_path)
            
            # Ensure the mirror directory structure exists
            os.makedirs(os.path.dirname(mirrored_dest_path), exist_ok=True)

            print(f"\n[INFO] Processing file: {file_path}")
            try:
                # Orchestrator saves to *._modern.py on success
                success = self.orchestrator.run_pipeline(file_path)
                
                if success:
                    # Move the generated modern file to the mirror directory
                    modern_file = file_path.replace(".py", "_modern.py")
                    if os.path.exists(modern_file):
                        shutil.copy2(modern_file, mirrored_dest_path)
                        print(f"[INFO] Saved modernized file to mirror: {mirrored_dest_path}")
                    else:
                        raise FileNotFoundError(f"Verified modern file not found: {modern_file}")
                else:
                    print(f"[FAIL] Orchestrator pipeline failed for {file_path}")
                    self.failed_files.append({
                        "file": file_path,
                        "error": "Pipeline returned False (verification failed or max retries reached)"
                    })

            except Exception as e:
                print(f"[ERROR] Exception during processing of {file_path}: {e}")
                self.failed_files.append({
                    "file": file_path,
                    "error": str(e)
                })

            processed_count += 1
            
            # Smart Rate Limit Handling: Wait 60 seconds after every 8 requests
            if processed_count % 8 == 0 and processed_count < len(files):
                print(f"[INFO] Rate limit safeguard: Waiting 60 seconds after {processed_count} files...")
                time.sleep(60)

        # Write failed files report
        if self.failed_files:
            print(f"\n[INFO] Saving failure report with {len(self.failed_files)} items to {self.report_path}")
            with open(self.report_path, "w") as f:
                json.dump(self.failed_files, f, indent=4)
        else:
            print(f"\n[INFO] All files processed successfully. No failures to report.")
            if os.path.exists(self.report_path):
                os.remove(self.report_path)

        print("\n[INFO] Batch processing complete.")
