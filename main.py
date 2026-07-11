import os
import shutil
import argparse
import sys

from src.utils.repo_manager import RepoManager
from src.utils.file_explorer import FileExplorer
from src.batch_processor import BatchProcessor
from src.utils.visualizer import MetricsVisualizer
from src.utils.report_generator import ReportGenerator

def clean_previous_logs():
    """Clears old metric and failure logs to ensure report accuracy."""
    os.makedirs("data", exist_ok=True)
    for file_path in ["data/evaluation_metrics.json", "data/failed_files_report.json"]:
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                print(f"[INFO] Cleared previous log: {file_path}")
            except Exception as e:
                print(f"[WARN] Could not clear log {file_path}: {e}")

def apply_modernized_files(modern_dir: str, repo_dir: str):
    """Copies refactored files back to cloned repo, overwriting original legacy files."""
    print("[INFO] Applying modernized files to repository...")
    for root, dirs, files in os.walk(modern_dir):
        for file in files:
            src_path = os.path.join(root, file)
            rel_path = os.path.relpath(src_path, modern_dir)
            dest_path = os.path.join(repo_dir, rel_path)
            
            # Ensure folder structure exists in destination
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            shutil.copy2(src_path, dest_path)
            print(f"[INFO] Applied refactored code to: {dest_path}")

def clean_intermediate_files(repo_dir: str):
    """Deletes temporary generated *_modern.py and *_modern_attempt_*.py files in cloned repo."""
    print("[INFO] Cleaning up intermediate code generation files...")
    deleted_count = 0
    for root, dirs, files in os.walk(repo_dir):
        for file in files:
            if file.endswith("_modern.py") or "_modern_attempt_" in file:
                file_path = os.path.join(root, file)
                try:
                    os.remove(file_path)
                    deleted_count += 1
                except Exception as e:
                    print(f"[WARN] Failed to delete intermediate file {file_path}: {e}")
    print(f"[INFO] Deleted {deleted_count} intermediate generation files.")

def main():
    parser = argparse.ArgumentParser(
        description="NeSyMA MK-2: Neuro-Symbolic Code Modernization & Verification Pipeline"
    )
    parser.add_argument(
        "--repo", 
        required=True, 
        help="Git repository URL to clone and modernize"
    )
    parser.add_argument(
        "--branch", 
        default="ai-refactored-v1", 
        help="Branch name to commit refactored changes to (default: ai-refactored-v1)"
    )
    parser.add_argument(
        "--commit-msg", 
        default="Refactor legacy code with Neuro-Symbolic AI", 
        help="Commit message for refactored changes"
    )
    parser.add_argument(
        "--clone-dir", 
        default="data/temp_repo", 
        help="Target folder to clone repository into (default: data/temp_repo)"
    )
    parser.add_argument(
        "--out-dir", 
        default="data/modernized_repo", 
        help="Folder to store refactored outputs (default: data/modernized_repo)"
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Optionally limit processing to N files for test execution"
    )
    
    args = parser.parse_args()

    print("\n" + "="*80)
    print("      NESYMA MK-2: NEURO-SYMBOLIC CODE MODERNIZATION & VERIFICATION PIPELINE      ")
    print("="*80)
    print(f"Target Repository: {args.repo}")
    print(f"Branch Name      : {args.branch}")
    print(f"Clone Directory  : {args.clone_dir}")
    print(f"Output Directory : {args.out_dir}")
    print("="*80 + "\n")

    # 1. Clear logs of previous runs
    clean_previous_logs()

    try:
        # 2. Clone repository
        repo_manager = RepoManager()
        repo_manager.clone_repo(args.repo, args.clone_dir)

        # 3. Discover python files
        explorer = FileExplorer()
        py_files = explorer.discover_files(args.clone_dir)
        print(f"[INFO] Discovered {len(py_files)} Python files inside repository.")

        if not py_files:
            print("[WARN] No Python files discovered in the cloned repository. Stopping pipeline.")
            sys.exit(0)

        # Apply file limit if specified
        if args.limit is not None and args.limit > 0:
            print(f"[INFO] Limiting processing to first {args.limit} files for testing.")
            py_files = py_files[:args.limit]

        # 4. Process files through orchestrator (refactoring & verifier)
        processor = BatchProcessor(source_dir=args.clone_dir, target_dir=args.out_dir)
        processor.process_files(py_files)

        # 5. Overwrite legacy files in cloned repository with modernized versions
        apply_modernized_files(args.out_dir, args.clone_dir)

        # 6. Clean up the intermediate helper files to keep the git history clean
        clean_intermediate_files(args.clone_dir)

        # 7. Commit changes to branch
        repo_manager.commit_and_branch(args.clone_dir, args.branch, args.commit_msg)

        print("\n" + "-"*50)
        print("[INFO] Running analytics and report generation...")
        print("-"*50)

        # 8. Generate visualization charts
        visualizer = MetricsVisualizer()
        visualizer.generate_plots()

        # 9. Generate Markdown report
        report_generator = ReportGenerator()
        report_generator.generate_report()

        print("\n" + "="*80)
        print("                            PIPELINE COMPLETED SUCCESSFULLY!                      ")
        print("="*80)
        print(f"Modernized repository changes committed in branch: '{args.branch}'")
        print("Examiner report generated: Thesis_Execution_Report.md")
        print("Analytics graphs saved in the 'data/' folder.")
        print("="*80 + "\n")

    except Exception as e:
        print(f"\n[FATAL ERROR] Pipeline failed: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
