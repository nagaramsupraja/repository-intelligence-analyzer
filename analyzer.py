import os
import ast


def analyze_python_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        source = file.read()

    tree = ast.parse(source)

    functions = [
        node.name
        for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    ]

    classes = [
        node.name
        for node in ast.walk(tree)
        if isinstance(node, ast.ClassDef)
    ]

    lines = len(source.splitlines())

    return {
        "file": file_path,
        "lines": lines,
        "functions": functions,
        "classes": classes,
    }


def analyze_repository(repo_path):
    results = []

    for root, dirs, files in os.walk(repo_path):
        # Don't analyze the virtual environment
        dirs[:] = [d for d in dirs if d != "venv" and d != ".git"]

        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                results.append(analyze_python_file(path))

    return results
def find_import_dependencies(repo_path):
    dependencies = {}

    for root, dirs, files in os.walk(repo_path):
        dirs[:] = [d for d in dirs if d != "venv" and d != ".git"]

        for file in files:
            if not file.endswith(".py"):
                continue

            path = os.path.join(root, file)

            with open(path, "r", encoding="utf-8") as f:
                source = f.read()

            tree = ast.parse(source)

            imports = []

            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for name in node.names:
                        imports.append(name.name)

                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        imports.append(node.module)

            dependencies[file] = imports

    return dependencies
def find_affected_files(repo_path, changed_file):
    dependencies = find_import_dependencies(repo_path)

    # Get only the filename
    changed_name = os.path.splitext(os.path.basename(changed_file))[0]

    affected = []

    for file, imports in dependencies.items():
        if file == changed_file:
            continue

        for imported_module in imports:
            imported_name = imported_module.split(".")[-1]

            if imported_name == changed_name:
                affected.append(file)
                break

    return affected
def get_changed_files(repo):
    latest_commit = repo.head.commit

    if not latest_commit.parents:
        return []

    parent = latest_commit.parents[0]

    changed_files = []

    for change in parent.diff(latest_commit):
        if change.a_path:
            changed_files.append(change.a_path)

    return changed_files