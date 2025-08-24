import os
import filecmp
import argparse
import json

def compare_repos(repo1, repo2, repo1_name, repo2_name, base=''):
    comparison = filecmp.dircmp(repo1, repo2)

    result = {
        "different": [],
        f"only_in_{repo1_name}": [],
        f"only_in_{repo2_name}": []
    }

    for file_name in comparison.common_files:
        file1 = os.path.join(repo1, file_name)
        file2 = os.path.join(repo2, file_name)
        rel_path = os.path.join(base, file_name)

        if not filecmp.cmp(file1, file2, shallow=False):
            result["different"].append(rel_path)

    result[f"only_in_{repo1_name}"].extend(os.path.join(base, f) for f in comparison.left_only)
    result[f"only_in_{repo2_name}"].extend(os.path.join(base, f) for f in comparison.right_only)

    for subdir in comparison.common_dirs:
        sub_result = compare_repos(
            os.path.join(repo1, subdir),
            os.path.join(repo2, subdir),
            repo1_name,
            repo2_name,
            base=os.path.join(base, subdir)
        )
        for key in result:
            result[key].extend(sub_result[key])

    return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("repo1")
    parser.add_argument("repo2")
    args = parser.parse_args()

    repo1_name = os.path.basename(os.path.normpath(args.repo1))
    repo2_name = os.path.basename(os.path.normpath(args.repo2))

    differences = compare_repos(args.repo1, args.repo2, repo1_name, repo2_name)
    print(json.dumps(differences, indent=2))
