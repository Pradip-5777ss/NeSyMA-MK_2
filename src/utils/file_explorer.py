import os
from typing import List

class FileExplorer:
    def __init__(self):
        self.ignore_dirs = {'.git', 'venv', '__pycache__', 'node_modules', 'env', '.venv'}
        
    def discover_files(self, directory: str) -> List[str]:
        """
        Scans a directory recursively to find all Python files,
        ignoring specified directories like .git, venv, etc.
        """
        py_files = []
        for root, dirs, files in os.walk(directory):
            # Modify dirs in-place to ignore certain directories
            dirs[:] = [d for d in dirs if d not in self.ignore_dirs]
            
            for file in files:
                if file.endswith('.py'):
                    full_path = os.path.join(root, file)
                    py_files.append(full_path)
                    
        return py_files
