import os
import json
from datetime import datetime

class ReportGenerator:
    def __init__(self, metrics_path: str = "data/evaluation_metrics.json",
                 failures_path: str = "data/failed_files_report.json",
                 output_path: str = "Thesis_Execution_Report.md"):
        self.metrics_path = metrics_path
        self.failures_path = failures_path
        self.output_path = output_path

    def generate_report(self):
        """Generates a professional markdown report for examiners."""
        print(f"[INFO] Generating thesis execution report at {self.output_path}...")
        
        # Load metrics
        metrics = []
        if os.path.exists(self.metrics_path):
            try:
                with open(self.metrics_path, 'r') as f:
                    metrics = json.load(f)
            except Exception as e:
                print(f"[ERROR] Failed to load metrics: {e}")
        
        # Load failures
        failures = []
        if os.path.exists(self.failures_path):
            try:
                with open(self.failures_path, 'r') as f:
                    failures = json.load(f)
            except Exception as e:
                print(f"[ERROR] Failed to load failures: {e}")

        total_files = len(metrics)
        if total_files == 0:
            print("[WARN] No metrics data found. Report will contain default values.")
            success_count = 0
            failed_count = 0
            success_rate = 0.0
            avg_llm_time = 0.0
            avg_z3_time = 0.0
            avg_total_time = 0.0
        else:
            success_count = sum(1 for item in metrics if item.get("final_status") == "Success")
            failed_count = total_files - success_count
            success_rate = (success_count / total_files) * 100.0
            
            total_llm_time = sum(item.get("llm_generation_time_ms", 0) for item in metrics) / 1000.0
            total_z3_time = sum(item.get("z3_verification_time_ms", 0) for item in metrics) / 1000.0
            
            avg_llm_time = total_llm_time / total_files
            avg_z3_time = total_z3_time / total_files
            avg_total_time = avg_llm_time + avg_z3_time

        # Format Failed Files Table
        if failed_count == 0:
            failed_files_section = "*No failures occurred during this execution run. All files were successfully modernized and formally verified.*"
        else:
            failed_files_section = "| File Path | Error Description |\n| :--- | :--- |\n"
            # Map failures for easy access by file path
            failure_map = {item.get("file"): item.get("error") for item in failures}
            for item in metrics:
                if item.get("final_status") == "Failed":
                    filepath = item.get("file", "unknown")
                    error_msg = failure_map.get(filepath, item.get("error", "Verification failed or max retries reached"))
                    rel_filepath = os.path.relpath(filepath) if os.path.isabs(filepath) else filepath
                    failed_files_section += f"| `{rel_filepath}` | {error_msg} |\n"

        current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        report_content = f"""# Thesis Execution Report: Neuro-Symbolic Code Modernization

**Date:** {current_date}
**System Version:** NeSyMA MK-2 (Neuro-Symbolic Modernization Agent)

## 1. Executive Summary
This report presents the execution results of the Neuro-Symbolic Code Modernization pipeline. The framework leverages LLMs (Gemini Provider) for code refactoring and the Z3 Theorem Prover (SMT solver) for formal verification of semantic equivalence.

## 2. Key Performance Metrics

| Metric | Value |
| :--- | :--- |
| **Total Files Processed** | {total_files} |
| **Successful Refactorings** | {success_count} |
| **Failed Refactorings** | {failed_count} |
| **Overall Success Rate** | **{success_rate:.2f}%** |
| **Average LLM Generation Time** | {avg_llm_time:.2f} seconds |
| **Average Z3 Verification Time** | {avg_z3_time:.2f} seconds |
| **Average Total Time per File** | **{avg_total_time:.2f} seconds** |

## 3. Visualizations

### Success vs. Failure Rate
![Success vs Failure](data/success_vs_failure.png)

### Execution Time Breakdown
![Time Analysis](data/time_analysis.png)

## 4. Failed Files Log
{failed_files_section}

## 5. Architectural Overview
The NeSyMA MK-2 framework operates in two distinct phases:
1. **Neural Phase (Generative AI):** The legacy Python code is analyzed, and the `GeminiProvider` refactors it into modernized Python syntax (incorporating type annotations, list comprehensions, etc.).
2. **Symbolic Phase (Verification):** Both legacy and modernized codes are parsed into ASTs using a Tree-Sitter based `LegacyCodeParser`. A `Z3Translator` extracts mathematical assertions from these ASTs, and the `EquivalenceVerifier` queries Z3 SMT solver to formally prove or disprove equivalence.

---
*Generated automatically by NeSyMA-MK_2 Report Generator.*
"""
        with open(self.output_path, 'w') as f:
            f.write(report_content)
            
        print(f"[SUCCESS] Thesis Execution Report written to {self.output_path}")
