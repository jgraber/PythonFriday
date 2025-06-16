import os
import subprocess

def run_git_fetch_all(root_path):
    for item in os.listdir(root_path):
        subdir_path = os.path.join(root_path, item)
        if os.path.isdir(subdir_path):
            print(f"Running 'git fetch --all' in: {subdir_path}")
            try:
                result = subprocess.run(["git", "fetch", "--all"], cwd=subdir_path, capture_output=True, text=True)
                print(result.stdout)
                if result.stderr:
                    print("Errors:", result.stderr)
            except Exception as e:
                print(f"Failed to run git fetch in {subdir_path}: {e}")


if __name__ == "__main__":
    run_git_fetch_all(r"C:\_GIT_BACKUP")
