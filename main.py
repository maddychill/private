import os
import random
import subprocess
from datetime import datetime, timedelta

MIN_COMMITS_PER_DAY = 6
MAX_COMMITS_PER_DAY = 12

def get_positive_int(prompt, default=100):
    while True:
        try:
            user_input = input(f"{prompt} (default {default}): ")
            if not user_input.strip():
                return default
            value = int(user_input)
            if value > 0:
                return value
            else:
                print("Enter a positive integer.")
        except ValueError:
            print("Invalid number.")

def random_day_in_last_year():
    today = datetime.now()
    start = today - timedelta(days=365)
    random_days = random.randint(0, 364)
    return start + timedelta(days=random_days)

def random_time_on_day(day):
    seconds = random.randint(0, 86399)
    return day + timedelta(seconds=seconds)

def make_commit(date, repo_path, filename):
    filepath = os.path.join(repo_path, filename)

    with open(filepath, "a") as f:
        f.write(f"Commit at {date}\n")

    subprocess.run(["git", "add", filename], cwd=repo_path)

    env = os.environ.copy()
    date_str = date.strftime("%Y-%m-%dT%H:%M:%S")
    env["GIT_AUTHOR_DATE"] = date_str
    env["GIT_COMMITTER_DATE"] = date_str

    subprocess.run(["git", "commit", "-m", "graph-greener"], cwd=repo_path, env=env)

def main():

    total_commits = get_positive_int("How many commits do you want", 100)
    repo_path = input("Repo path (default .): ") or "."
    filename = input("Filename (default data.txt): ") or "data.txt"

    commits_done = 0

    print("\nGenerating commits...\n")

    while commits_done < total_commits:

        day = random_day_in_last_year()

        commits_today = random.randint(
            MIN_COMMITS_PER_DAY,
            MAX_COMMITS_PER_DAY
        )

        for _ in range(commits_today):

            if commits_done >= total_commits:
                break

            commit_time = random_time_on_day(day)

            print(f"Commit {commits_done+1} at {commit_time}")

            make_commit(commit_time, repo_path, filename)

            commits_done += 1

    print("\nPushing to GitHub...")
    subprocess.run(["git", "push"], cwd=repo_path)

    print("Done!")

if __name__ == "__main__":
    main()