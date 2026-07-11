import os
import time
from src.utils.repo_manager import RepoManager
from src.utils.file_explorer import FileExplorer
from src.batch_processor import BatchProcessor

def main():
    repo_url = "https://github.com/octocat/Spoon-Knife" # Very small repo
    # Or maybe a small python repo: "https://github.com/pallets/itsdangerous"
    repo_url = "https://github.com/pallets/itsdangerous"
    target_dir = "data/temp_repo"
    modernized_dir = "data/modernized_repo"
    
    print("=== Phase 4 End-to-End Testing ===")
    start_time = time.time()
    
    # 1. Clone Repo
    repo_manager = RepoManager()
    repo_manager.clone_repo(repo_url, target_dir)
    
    # 2. Discover Files
    explorer = FileExplorer()
    py_files = explorer.discover_files(target_dir)
    print(f"[INFO] Discovered {len(py_files)} Python files.")
    
    # For testing purposes, we limit to 2 files to avoid excessive API calls and time
    test_files = py_files[:2]
    print(f"[INFO] Limiting to {len(test_files)} files for quick testing.")
    
    # 3. Batch Process
    processor = BatchProcessor(source_dir=target_dir, target_dir=modernized_dir)
    processor.process_files(test_files)
    
    # 4. Commit and Branch
    # We commit in the modernized_dir to simulate the pipeline creating a new branch
    # But wait, the prompt says: "create a new branch named ai-refactored-v1 and automatically commit the code"
    # Usually we commit the modernized code over the old code or in the original repo.
    # Let's commit in the temp_repo since that's a git repo.
    # We'll copy modernized files back to temp_repo first.
    print("[INFO] Applying modernized files to repository...")
    import shutil
    for root, dirs, files in os.walk(modernized_dir):
        for file in files:
            src_path = os.path.join(root, file)
            rel_path = os.path.relpath(src_path, modernized_dir)
            dest_path = os.path.join(target_dir, rel_path)
            shutil.copy2(src_path, dest_path)
    
    repo_manager.commit_and_branch(target_dir, "ai-refactored-v1", "Refactored legacy code with Neuro-Symbolic AI")
    
    end_time = time.time()
    
    # Summary
    total_files = len(test_files)
    failed = len(processor.failed_files)
    success = total_files - failed
    success_rate = (success / total_files * 100) if total_files > 0 else 0
    
    print("\n=== Pipeline Summary ===")
    print(f"Total files processed: {total_files}")
    print(f"Success rate: {success_rate:.2f}%")
    print(f"Time taken: {end_time - start_time:.2f} seconds")

if __name__ == "__main__":
    main()
