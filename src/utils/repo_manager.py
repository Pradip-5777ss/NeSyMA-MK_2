import os
import shutil
from git import Repo

class RepoManager:
    def __init__(self):
        pass

    def clone_repo(self, repo_url: str, target_dir: str) -> Repo:
        """
        Clones a repository from repo_url into target_dir.
        If target_dir already exists, it removes it first.
        """
        print(f"[INFO] Cloning repository {repo_url} into {target_dir}...")
        if os.path.exists(target_dir):
            print(f"[INFO] Removing existing directory at {target_dir}...")
            shutil.rmtree(target_dir)
            
        repo = Repo.clone_from(repo_url, target_dir)
        print("[INFO] Clone successful.")
        return repo

    def commit_and_branch(self, repo_dir: str, branch_name: str, message: str):
        """
        Creates a new branch, adds all changes, and commits them.
        """
        print(f"[INFO] Committing changes to branch {branch_name} in {repo_dir}...")
        repo = Repo(repo_dir)
        
        # Create new branch
        new_branch = repo.create_head(branch_name)
        new_branch.checkout()
        
        # Add all changes
        repo.git.add(A=True)
        
        # Commit
        repo.index.commit(message)
        print(f"[SUCCESS] Committed changes to {branch_name} with message: '{message}'")
