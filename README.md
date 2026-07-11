# NeSyMA MK-2: Neuro-Symbolic Modernization Agent

NeSyMA MK-2 is an advanced framework that automates the translation of legacy Python source code into modern, optimized Python syntax while providing a formal guarantee of semantic equivalence using the Z3 Theorem Prover.

It features a dual-phase architecture:
1. **Neural Phase (Generative AI):** Employs LLMs (via Gemini API) to perform advanced code refactoring (e.g., modernizing loop statements, adding type hints, using list comprehensions).
2. **Symbolic Phase (Verification):** Extracts logic constraints from the legacy and refactored ASTs using Tree-Sitter, translates them to SMT formulas, and queries the Z3 Theorem Prover to formally prove semantic equivalence.

---

## 🗺️ System Architecture

The following diagram illustrates the complete end-to-end modernization and verification pipeline:

```mermaid
graph TD
    A[Git Repository URL] -->|1. Clone Repo| B[RepoManager]
    B -->|2. Scans Directory| C[FileExplorer]
    C -->|3. Discovers Python Files| D[BatchProcessor]
    D -->|4. Processes File by File| E[Neuro-Symbolic Orchestrator]
    
    subgraph "Orchestrator Pipeline (In-Loop Refactor & Verify)"
        E -->|Read File| F[Legacy Code]
        F -->|Parse AST| G[LegacyCodeParser]
        G -->|Extract Logic| H[Z3Translator (L_)]
        
        E -->|Refactor Request| I[GeminiProvider]
        I -->|Generate| J[Modernized Code]
        J -->|Parse AST| K[ModernCodeParser]
        K -->|Extract Logic| L[Z3Translator (M_)]
        
        H -->|Constraints| M[EquivalenceVerifier]
        L -->|Constraints| M
        M -->|Queries Z3 Solver| N{Equivalent?}
        
        N -->|No: Feedbacks Errors| I
        N -->|Yes: Save Code| O[Modernized Output File]
    end
    
    D -->|5. Apply Refactored Files| P[Cloned Repo Git Tree]
    P -->|6. Commit & Branch| Q[New Branch: ai-refactored-v1]
    
    D -->|7. Write Logs| R[evaluation_metrics.json]
    R -->|8. Generate Graphs| S[MetricsVisualizer]
    R -->|9. Compile Report| T[ReportGenerator]
    
    S -->|PNG Plots| U[Thesis_Execution_Report.md]
    T -->|Markdown| U
```

---

## 🛠️ Environment Setup

### 1. Prerequisites
- Python 3.10 or higher
- Git installed on your system

### 2. Installation
Clone the repository and install all required dependencies:
```bash
git clone <repository_url>
cd NeSyMA-MK_2
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. API Credentials
Create a `.env` file in the project root directory and add your Gemini API Key:
```env
GEMINI_API_KEY=your_gemini_api_key_here
```

---

## 🚀 Execution Commands

Execute the entire end-to-end pipeline with a single CLI command:

```bash
python main.py --repo "https://github.com/user/project.git"
```

### Advanced CLI Arguments

| Argument | Description | Default |
| :--- | :--- | :--- |
| `--repo` | **(Required)** The git repository URL to clone and refactor. | N/A |
| `--branch` | The name of the git branch to commit modernized files into. | `ai-refactored-v1` |
| `--commit-msg` | The message to commit the changes with. | `Refactor legacy code with Neuro-Symbolic AI` |
| `--clone-dir` | Path to the directory where the target repository will be cloned. | `data/temp_repo` |
| `--out-dir` | Path to the directory where refactored files are stored. | `data/modernized_repo` |
| `--limit` | Limit processing to first N files (ideal for testing). | `None` (All files) |

#### Example: Running a quick test on the first 2 files of a repo
```bash
python main.py --repo "https://github.com/pallets/itsdangerous.git" --limit 2
```

---

## 📊 Analytics & Examiner Reports

At the end of execution, NeSyMA MK-2 automatically runs post-processing hooks to create evaluation artifacts:
1. **Thesis_Execution_Report.md:** A professionally formatted report containing success rates, average time breakdown, and detailed logs of any failed files.
2. **Visualizations:**
   - `data/success_vs_failure.png`: A pie chart showing the pipeline's success rate.
   - `data/time_analysis.png`: A stacked bar chart visualizing time spent on LLM generation versus Z3 verification for each file.

---
*Created as part of the Neuro-Symbolic Software Engineering Research Framework.*
