import os
import shutil
import requests
from datetime import datetime

# GitHub Configuration
GITHUB_USERNAME = "your_username"
TOKEN = "your_personal_access_token"
BASE_URL = "https://api.github.com"

# Repository details
REPO_NAME = "test_script"

def create_repository():
    url = f"{BASE_URL}/user/repos"
    headers = {"Authorization": f"token {TOKEN}"}
    data = {"name": REPO_NAME, "auto_init": True}
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 201:
        print("Repository created successfully!")
        return response.json()["clone_url"]
    else:
        print("Error creating repository:", response.json())
        return None

def make_commits(repo_dir):
    for i in range(1, 21):
        file_path = os.path.join(repo_dir, f"file_{i}.txt")
        with open(file_path, "w") as f:
            f.write(f"Commit {i}: {datetime.now()}")
        os.system(f"cd {repo_dir} && git add . && git commit -m 'Commit {i}'")

def delete_repository():
    url = f"{BASE_URL}/repos/{GITHUB_USERNAME}/{REPO_NAME}"
    headers = {"Authorization": f"token {TOKEN}"}
    response = requests.delete(url, headers=headers)
    if response.status_code == 204:
        print("Repository deleted successfully!")
    else:
        print("Error deleting repository:", response.json())

def main():
    # Step 1: Create repository
    clone_url = create_repository()
    if not clone_url:
        return

    # Step 2: Clone the repository locally
    repo_dir = os.path.join(os.getcwd(), REPO_NAME)
    os.system(f"git clone {clone_url} {repo_dir}")

    # Step 3: Make 20 commits
    make_commits(repo_dir)

    # Step 4: Push changes
    os.system(f"cd {repo_dir} && git push origin main")

    # Step 5: Delete the repository
    delete_repository()

    # Cleanup: Remove local repo
    shutil.rmtree(repo_dir)

if __name__ == "__main__":
    main()
