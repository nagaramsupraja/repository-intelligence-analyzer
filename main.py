from utils import calculate_sum
from git import Repo
from analyzer import (
    analyze_repository,
    find_import_dependencies,
    find_affected_files,
    get_changed_files
)

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

# Analyzer test
print("\nAnalyzer is ready!")
print("Test result:", calculate_sum(10, 20))


print("\nRepository Analysis")
print("-------------------")

results = analyze_repository(repo.working_tree_dir)

print("Python Files:", len(results))

for result in results:
    print("\nFile:", result["file"])
    print("Lines:", result["lines"])
    print("Functions:", result["functions"])
    print("Classes:", result["classes"])
    print("\nImport Dependencies")
print("-------------------")

dependencies = find_import_dependencies(repo.working_tree_dir)

for file, imports in dependencies.items():
    print("\n", file)
    print("Imports:", imports)
    print("\nChange Impact Analysis")
print("----------------------")
print("\nAutomatic Change Impact Analysis")
print("--------------------------------")

changed_files = get_changed_files(repo)

if not changed_files:
    print("No changed files found.")
else:
    for changed_file in changed_files:
        print("\nChanged file:", changed_file)

        affected_files = find_affected_files(
            repo.working_tree_dir,
            changed_file
        )

        if affected_files:
            print("Potentially affected files:")
            for file in affected_files:
                print("-", file)
        else:
            print("No affected files found.")
            print("\nAnalysis Summary")
print("----------------")

print("Total Python files:", len(results))
print("Total changed files:", len(changed_files))

total_affected = 0

for changed_file in changed_files:
    affected_files = find_affected_files(
        repo.working_tree_dir,
        changed_file
    )
    total_affected += len(affected_files)

print("Total potentially affected files:", total_affected)

print("\nAnalyzer completed successfully!")
  