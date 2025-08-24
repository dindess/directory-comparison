import os
import filecmp
import argparse
import json

def compare_repos(repo1, repo2, repo1_key, repo2_key, base=''):
    comparison = filecmp.dircmp(repo1, repo2)

    result = {
        "different": [],
        f"only_in_{repo1_key}": [],
        f"only_in_{repo2_key}": []
    }

    for file_name in comparison.common_files:
        file1 = os.path.join(repo1, file_name)
        file2 = os.path.join(repo2, file_name)
        rel_path = os.path.join(base, file_name)

        if not filecmp.cmp(file1, file2, shallow=False):
            result["different"].append(rel_path)

    result[f"only_in_{repo1_key}"].extend(os.path.join(base, f) for f in comparison.left_only)
    result[f"only_in_{repo2_key}"].extend(os.path.join(base, f) for f in comparison.right_only)

    for subdir in comparison.common_dirs:
        sub_result = compare_repos(
            os.path.join(repo1, subdir),
            os.path.join(repo2, subdir),
            repo1_key,
            repo2_key,
            base=os.path.join(base, subdir)
        )
        for key in result:
            result[key].extend(sub_result[key])

    return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compare two directories and show only differences as JSON")
    parser.add_argument("repo1", help="First repository path")
    parser.add_argument("repo2", help="Second repository path")
    args = parser.parse_args()

    repo1_abs = os.path.abspath(args.repo1)
    repo2_abs = os.path.abspath(args.repo2)

    differences = compare_repos(args.repo1, args.repo2, repo1_abs, repo2_abs)
    print(json.dumps(differences, indent=2))
