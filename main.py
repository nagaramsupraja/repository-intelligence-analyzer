import sys
from git import Repo
from utils import calculate_sum
from analyzer import (
    analyze_repository,
    find_import_dependencies,
    find_affected_files,
    get_changed_files
)


def main():

    # Get repository path from command line
    if len(sys.argv) > 1:
        repo_path = sys.argv[1]
    else:
        repo_path = "."

    try:
        repo = Repo(repo_path)
    except Exception:
        print("Error: The given path is not a valid Git repository.")
        return

    print("Repository Intelligence Analyzer")
    print("---------------------------------")

    print("Current branch:", repo.active_branch.name)
    print("Repository path:", repo.working_tree_dir)

    # Commit history
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

    # Changed files
    print("\nChanged Files")
    print("-------------")

    changed_files = get_changed_files(repo)

    if changed_files:
        for changed_file in changed_files:
            print("-", changed_file)
    else:
        print("No changed files found.")

    # Repository analysis
    print("\nRepository Analysis")
    print("-------------------")

    results = analyze_repository(repo.working_tree_dir)

    print("Total Python files:", len(results))

    for result in results:
        print("\nFile:", result["file"])
        print("Lines:", result["lines"])
        print("Functions:", result["functions"])
        print("Classes:", result["classes"])

    # Import dependencies
    print("\nImport Dependencies")
    print("-------------------")

    dependencies = find_import_dependencies(repo.working_tree_dir)

    for file, imports in dependencies.items():
        print("\n", file)
        print("Imports:", imports)

    # Change impact analysis
    print("\nChange Impact Analysis")
    print("----------------------")

    total_affected = 0

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

            total_affected += len(affected_files)

        else:
            print("No affected files found.")

    # Summary
    print("\nAnalysis Summary")
    print("----------------")

    print("Total Python files:", len(results))
    print("Total changed files:", len(changed_files))
    print("Total potentially affected files:", total_affected)

    print("\nAnalyzer completed successfully!")


if __name__ == "__main__":
    main()