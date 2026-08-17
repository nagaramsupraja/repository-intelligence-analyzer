from git import Repo

repo = Repo(".")

print("Repository Intelligence Analyzer")
print("---------------------------------")

print("Current branch:", repo.active_branch.name)
print("Repository path:", repo.working_tree_dir)

print("\nCommit History")
print("-------------")

for commit in repo.iter_commits():
    print(commit.hexsha[:8], "-", commit.message.strip())

# Latest commit
latest_commit = repo.head.commit

print("\nLatest Commit")
print("-------------")
print("Commit:", latest_commit.hexsha[:8])
print("Message:", latest_commit.message.strip())

print("\nChanged Files")
print("-------------")

if latest_commit.parents:
    parent = latest_commit.parents[0]

    for change in parent.diff(latest_commit):
        print(change.change_type, "-", change.a_path)
else:
    print("This is the first commit; no previous commit to compare with.")
    print("\nAnalyzer is ready!")